import asyncio
import hmac
import os
import time
from typing import Any, Literal

import httpx
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Deep Reasoning Gateway",
    version="0.1.0",
    description=(
        "A small orchestration layer that increases real model work through OpenAI "
        "reasoning controls and multi-pass review. It does not modify ChatGPT's hidden runtime."
    ),
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6")
GATEWAY_TOKEN = os.getenv("GATEWAY_TOKEN", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
POLL_INTERVAL_SECONDS = float(os.getenv("POLL_INTERVAL_SECONDS", "1.5"))
POLL_TIMEOUT_SECONDS = float(os.getenv("POLL_TIMEOUT_SECONDS", "900"))
MAX_PROMPT_CHARS = int(os.getenv("MAX_PROMPT_CHARS", "50000"))
MAX_CONCURRENCY = int(os.getenv("MAX_CONCURRENCY", "2"))

_SEMAPHORE = asyncio.Semaphore(MAX_CONCURRENCY)

Effort = Literal["low", "medium", "high", "xhigh", "max"]
Mode = Literal["standard", "pro"]
Strategy = Literal["single", "deep"]


class ThinkRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=100000)
    effort: Effort = "max"
    mode: Mode = "pro"
    strategy: Strategy = "deep"
    max_output_tokens: int = Field(default=4000, ge=128, le=32000)


class PassMetric(BaseModel):
    name: str
    elapsed_ms: int
    response_id: str | None = None
    usage: dict[str, Any] | None = None


class ThinkResponse(BaseModel):
    answer: str
    model: str
    strategy: Strategy
    effort: Effort
    mode: Mode
    total_elapsed_ms: int
    passes: list[PassMetric]


def _require_gateway_token(authorization: str | None) -> None:
    if not GATEWAY_TOKEN:
        raise HTTPException(status_code=503, detail="GATEWAY_TOKEN is not configured")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    provided = authorization.removeprefix("Bearer ").strip()
    if not hmac.compare_digest(provided, GATEWAY_TOKEN):
        raise HTTPException(status_code=401, detail="Invalid bearer token")


def _extract_output_text(payload: dict[str, Any]) -> str:
    chunks: list[str] = []
    for item in payload.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text" and content.get("text"):
                chunks.append(content["text"])
    text = "\n".join(chunks).strip()
    if not text:
        raise HTTPException(status_code=502, detail="OpenAI response contained no output text")
    return text


def _safe_usage(payload: dict[str, Any]) -> dict[str, Any] | None:
    usage = payload.get("usage")
    return usage if isinstance(usage, dict) else None


async def _run_model(
    *,
    input_text: str,
    effort: Effort,
    mode: Mode,
    max_output_tokens: int,
    instructions: str,
) -> tuple[str, PassMetric]:
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=503, detail="OPENAI_API_KEY is not configured")

    payload: dict[str, Any] = {
        "model": OPENAI_MODEL,
        "input": input_text,
        "instructions": instructions,
        "reasoning": {"effort": effort, "mode": mode},
        "max_output_tokens": max_output_tokens,
        "background": True,
        "store": False,
    }
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    started = time.perf_counter()
    timeout = httpx.Timeout(connect=15.0, read=30.0, write=30.0, pool=15.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        created = await client.post(f"{OPENAI_BASE_URL}/responses", headers=headers, json=payload)
        if created.status_code >= 400:
            request_id = created.headers.get("x-request-id")
            raise HTTPException(
                status_code=502,
                detail=f"OpenAI create failed ({created.status_code}); request_id={request_id}",
            )
        response = created.json()
        response_id = response.get("id")
        deadline = time.monotonic() + POLL_TIMEOUT_SECONDS

        while response.get("status") in {"queued", "in_progress"}:
            if not response_id:
                raise HTTPException(status_code=502, detail="OpenAI background response missing id")
            if time.monotonic() >= deadline:
                raise HTTPException(status_code=504, detail="OpenAI background response timed out")
            await asyncio.sleep(POLL_INTERVAL_SECONDS)
            polled = await client.get(f"{OPENAI_BASE_URL}/responses/{response_id}", headers=headers)
            if polled.status_code >= 400:
                request_id = polled.headers.get("x-request-id")
                raise HTTPException(
                    status_code=502,
                    detail=f"OpenAI poll failed ({polled.status_code}); request_id={request_id}",
                )
            response = polled.json()

    status = response.get("status")
    if status != "completed":
        raise HTTPException(status_code=502, detail=f"OpenAI response ended with status={status}")

    elapsed_ms = int((time.perf_counter() - started) * 1000)
    metric = PassMetric(
        name="model_pass",
        elapsed_ms=elapsed_ms,
        response_id=response.get("id"),
        usage=_safe_usage(response),
    )
    return _extract_output_text(response), metric


@app.get("/healthz")
async def healthz() -> dict[str, Any]:
    return {
        "status": "ok",
        "model": OPENAI_MODEL,
        "openai_key_configured": bool(OPENAI_API_KEY),
        "gateway_token_configured": bool(GATEWAY_TOKEN),
        "max_concurrency": MAX_CONCURRENCY,
    }


@app.post("/v1/think", response_model=ThinkResponse)
async def think(request: ThinkRequest, authorization: str | None = Header(default=None)) -> ThinkResponse:
    _require_gateway_token(authorization)
    if len(request.prompt) > MAX_PROMPT_CHARS:
        raise HTTPException(status_code=413, detail=f"Prompt exceeds MAX_PROMPT_CHARS={MAX_PROMPT_CHARS}")

    started = time.perf_counter()
    passes: list[PassMetric] = []

    async with _SEMAPHORE:
        if request.strategy == "single":
            answer, metric = await _run_model(
                input_text=request.prompt,
                effort=request.effort,
                mode=request.mode,
                max_output_tokens=request.max_output_tokens,
                instructions=(
                    "Answer the user's request accurately. Do not reveal private chain-of-thought. "
                    "Give conclusions, key assumptions, calculations, and verifiable evidence when useful."
                ),
            )
            metric.name = "single"
            passes.append(metric)
        else:
            draft, metric = await _run_model(
                input_text=request.prompt,
                effort=request.effort,
                mode=request.mode,
                max_output_tokens=request.max_output_tokens,
                instructions=(
                    "Produce a strong candidate answer. Check assumptions and edge cases. "
                    "Do not reveal private chain-of-thought; output only the candidate answer."
                ),
            )
            metric.name = "draft"
            passes.append(metric)

            critique, metric = await _run_model(
                input_text=f"ORIGINAL REQUEST:\n{request.prompt}\n\nCANDIDATE ANSWER:\n{draft}",
                effort=request.effort,
                mode=request.mode,
                max_output_tokens=min(request.max_output_tokens, 6000),
                instructions=(
                    "Act as a rigorous reviewer. Identify concrete factual errors, missing constraints, "
                    "unsupported assumptions, and likely failure modes in the candidate. Do not reveal "
                    "private chain-of-thought; return only concise review findings and corrections."
                ),
            )
            metric.name = "critique"
            passes.append(metric)

            answer, metric = await _run_model(
                input_text=(
                    f"ORIGINAL REQUEST:\n{request.prompt}\n\nCANDIDATE ANSWER:\n{draft}"
                    f"\n\nREVIEW FINDINGS:\n{critique}"
                ),
                effort=request.effort,
                mode=request.mode,
                max_output_tokens=request.max_output_tokens,
                instructions=(
                    "Write the final answer. Correct every valid review finding, preserve the user's "
                    "requirements, and prefer verifiable conclusions. Do not reveal private chain-of-thought "
                    "or mention this internal review pipeline."
                ),
            )
            metric.name = "final"
            passes.append(metric)

    total_elapsed_ms = int((time.perf_counter() - started) * 1000)
    return ThinkResponse(
        answer=answer,
        model=OPENAI_MODEL,
        strategy=request.strategy,
        effort=request.effort,
        mode=request.mode,
        total_elapsed_ms=total_elapsed_ms,
        passes=passes,
    )
