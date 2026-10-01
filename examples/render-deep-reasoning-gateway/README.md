# Render Deep Reasoning Gateway

A deployable FastAPI gateway for **real additional model work** using the OpenAI Responses API.

It has two execution strategies:

- `single`: one model call using the requested `reasoning.effort` and `reasoning.mode`.
- `deep`: three model calls — candidate answer -> critique -> final correction — using the same requested reasoning settings on every pass.

The default deep profile is `effort=max`, `mode=pro`.

## What this does and does not do

This service can increase actual API-side model work, latency, reasoning-token use, and review depth. It **does not modify ChatGPT's hidden consumer runtime**, and it cannot turn an external API call into ordinary ChatGPT message quota. OpenAI API usage is billed separately from ChatGPT subscriptions.

For standard ChatGPT conversations, use the reasoning controls that ChatGPT exposes. If you want ChatGPT to invoke this gateway, connect it through a supported tool/plugin/app integration; the delegated gateway call still uses the API key configured on this service.

Do not simulate deeper reasoning with fixed sleep/wait time. Polling sleeps in this project exist only to retrieve asynchronous OpenAI background responses.

## Architecture

```text
client / ChatGPT tool integration
        |
        | Bearer GATEWAY_TOKEN
        v
Render FastAPI gateway
        |
        | OPENAI_API_KEY (server-side only)
        v
OpenAI Responses API
        |
        +-- single: one response
        |
        +-- deep: draft -> critique -> final
```

The API returns the final answer plus per-pass elapsed time and OpenAI usage metadata. It never returns hidden chain-of-thought.

## Endpoints

### `GET /healthz`

Returns service status and boolean configuration flags. It never returns secret values.

### `POST /v1/think`

Header:

```text
Authorization: Bearer <GATEWAY_TOKEN>
```

Example request:

```json
{
  "prompt": "Review this migration plan and identify failure modes.",
  "strategy": "deep",
  "effort": "max",
  "mode": "pro",
  "max_output_tokens": 4000
}
```

Example curl:

```bash
curl -sS https://YOUR-SERVICE.onrender.com/v1/think \
  -H "Authorization: Bearer $GATEWAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Review this migration plan and identify failure modes.",
    "strategy": "deep",
    "effort": "max",
    "mode": "pro"
  }'
```

## Local setup

```bash
cd examples/render-deep-reasoning-gateway
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements-dev.txt
cp .env.example .env       # do not commit .env
```

Export the real secrets into the shell before starting:

```bash
export OPENAI_API_KEY='...'
export GATEWAY_TOKEN='use-a-long-random-secret'
uvicorn main:app --host 127.0.0.1 --port 8000
```

Then:

```bash
pytest -q
curl http://127.0.0.1:8000/healthz
```

## Render deployment

The repository root contains `render.yaml` for a Render Blueprint.

1. In Render, create a new Blueprint from this GitHub repository and select the desired branch/revision.
2. Render reads `render.yaml` and uses `examples/render-deep-reasoning-gateway` as `rootDir`.
3. Set secret values when prompted:
   - `OPENAI_API_KEY`
   - `GATEWAY_TOKEN` (generate a long random value)
4. Deploy.
5. Confirm `/healthz` returns HTTP 200.
6. Send an authenticated `single` request first, then a `deep` request.
7. Run `benchmark.py` to compare latency, model-pass count, reasoning-token usage (when present), and smoke-test quality.

The Blueprint defaults to Render's `free` plan to avoid surprise infrastructure charges during proof-of-concept testing. For stable latency measurements, upgrade to `0.5c-512mb` or higher because free services can spin down when inactive, adding cold-start delay.

Render is a good fit for this gateway because model inference happens at OpenAI; the service mainly performs authentication, orchestration, HTTP I/O, and response aggregation. Heavy local CPU/GPU is not required.

## Live read-back benchmark

After deployment:

```bash
python benchmark.py \
  --url https://YOUR-SERVICE.onrender.com \
  --token "$GATEWAY_TOKEN" \
  --output benchmark-results.json
```

The benchmark compares:

- baseline: `single + medium + standard`
- candidate: `deep + max + pro`

Its `read_back` section reports four separate observations:

1. `more_model_work_observed`: deep executed more model passes.
2. `higher_wall_time_observed`: deep took longer end to end.
3. `reasoning_tokens_increased`: OpenAI reported more reasoning tokens when that usage field is available.
4. `quality_non_regression_on_cases`: the bundled deterministic smoke cases did not score worse.

The bundled quality test is deliberately small. For a production decision, use 20-100 representative prompts and blinded scoring rather than treating elapsed time as proof of intelligence.

## Recommended regression gate

Before promoting a new reasoning configuration:

- Use the same prompt set for baseline and candidate.
- Randomize answer order for human or model-assisted judging.
- Track task success / correctness separately from style preference.
- Track median and p95 latency.
- Track input, output, and reasoning-token usage where available.
- Require candidate correctness to be no worse than baseline on hard slices.
- Add a maximum acceptable cost/latency multiplier for your workload.
- Retest after model-version, prompt, or orchestration changes.

A slower result is **not** automatically a better result.

## Security notes

- Never put `OPENAI_API_KEY` or `GATEWAY_TOKEN` in Git.
- Keep both as Render environment secrets.
- The public `/v1/think` endpoint requires a bearer token.
- Rotate `GATEWAY_TOKEN` if it leaks.
- The gateway does not log prompts by default.
- OpenAI requests use `store=false` and background execution; background execution still requires temporary server-side storage for polling according to OpenAI's documented background-mode behavior.
- Limit prompt size and concurrency to control abuse and API spend.
- Put stronger identity/rate-limit controls in front of this service before exposing it to untrusted users.

## Performance notes

- Render web services support long HTTP responses, which makes them suitable for long-running LLM calls.
- Free instances are for prototyping; cold starts can contaminate latency measurements.
- Start at 0.5 CPU / 512 MB for light always-on traffic; increase to 1 CPU / 2 GB when concurrency or middleware load justifies it.
- OpenAI latency and token usage usually dominate the cost of this thin gateway.

## Current evidence sources

- OpenAI reasoning guide: https://developers.openai.com/api/docs/guides/reasoning
- OpenAI background mode: https://developers.openai.com/api/docs/guides/background
- ChatGPT GPT-5.6 controls: https://help.openai.com/en/articles/20001354-gpt-56-and-gpt-6-pro-in-chatgpt
- Render web services: https://render.com/docs/web-services
- Render Blueprint spec: https://render.com/docs/blueprint-spec
- Render pricing: https://render.com/pricing
