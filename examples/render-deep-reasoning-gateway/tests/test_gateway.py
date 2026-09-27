import os

os.environ["OPENAI_API_KEY"] = "test-openai-key"
os.environ["GATEWAY_TOKEN"] = "test-gateway-token"
os.environ["MAX_CONCURRENCY"] = "2"

from fastapi.testclient import TestClient

import main

client = TestClient(main.app)
AUTH = {"Authorization": "Bearer test-gateway-token"}


def test_healthz_reports_configuration_without_secrets():
    response = client.get("/healthz")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["openai_key_configured"] is True
    assert payload["gateway_token_configured"] is True
    assert "test-openai-key" not in response.text
    assert "test-gateway-token" not in response.text


def test_think_rejects_missing_bearer_token():
    response = client.post("/v1/think", json={"prompt": "hello"})
    assert response.status_code == 401


def test_single_strategy_runs_exactly_one_model_pass(monkeypatch):
    calls = []

    async def fake_run_model(**kwargs):
        calls.append(kwargs)
        return "single answer", main.PassMetric(name="model_pass", elapsed_ms=10, response_id="resp_single")

    monkeypatch.setattr(main, "_run_model", fake_run_model)
    response = client.post(
        "/v1/think",
        headers=AUTH,
        json={
            "prompt": "Solve carefully",
            "strategy": "single",
            "effort": "medium",
            "mode": "standard",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["answer"] == "single answer"
    assert len(calls) == 1
    assert len(payload["passes"]) == 1
    assert payload["passes"][0]["name"] == "single"
    assert calls[0]["effort"] == "medium"
    assert calls[0]["mode"] == "standard"


def test_deep_strategy_runs_three_real_model_passes(monkeypatch):
    calls = []
    outputs = iter(["draft answer", "review findings", "final corrected answer"])

    async def fake_run_model(**kwargs):
        calls.append(kwargs)
        index = len(calls)
        return next(outputs), main.PassMetric(
            name="model_pass",
            elapsed_ms=10,
            response_id=f"resp_{index}",
            usage={"output_tokens": 100 * index},
        )

    monkeypatch.setattr(main, "_run_model", fake_run_model)
    response = client.post(
        "/v1/think",
        headers=AUTH,
        json={
            "prompt": "Analyze a difficult problem",
            "strategy": "deep",
            "effort": "max",
            "mode": "pro",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["answer"] == "final corrected answer"
    assert len(calls) == 3
    assert [item["name"] for item in payload["passes"]] == ["draft", "critique", "final"]
    assert all(call["effort"] == "max" for call in calls)
    assert all(call["mode"] == "pro" for call in calls)
    assert "draft answer" in calls[1]["input_text"]
    assert "review findings" in calls[2]["input_text"]


def test_invalid_effort_fails_validation():
    response = client.post(
        "/v1/think",
        headers=AUTH,
        json={"prompt": "hello", "effort": "infinite"},
    )
    assert response.status_code == 422
