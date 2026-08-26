import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export type AdaptiveResult = Record<string, unknown>;

const HERE = path.dirname(fileURLToPath(import.meta.url));
const SCRIPTS_DIR = path.resolve(HERE, "../../../scripts");
const HEALTH_SCRIPT = path.join(SCRIPTS_DIR, "capability_health.py");
const ROUTER_SCRIPT = path.join(SCRIPTS_DIR, "capability_router.py");

function pythonBin(): string {
  return process.env.PYTHON_BIN?.trim() || "python3";
}

function timeoutMs(): number {
  const raw = Number(process.env.ORDINARY_CHAT_ADAPTIVE_TIMEOUT_MS ?? 5000);
  if (!Number.isFinite(raw)) return 5000;
  return Math.min(30000, Math.max(500, Math.trunc(raw)));
}

function runFixedScript(script: string, args: string[]): AdaptiveResult {
  if (!fs.existsSync(script)) {
    return { schemaVersion: 1, result: "BLOCKED", reason: "adaptive_script_missing" };
  }
  const cp = spawnSync(pythonBin(), [script, ...args], {
    encoding: "utf8",
    timeout: timeoutMs(),
    maxBuffer: 2 * 1024 * 1024,
    env: process.env,
  });
  if (cp.error) {
    return {
      schemaVersion: 1,
      result: "BLOCKED",
      reason: `adaptive_spawn_error:${cp.error.name}`,
    };
  }
  if (!cp.stdout?.trim()) {
    return {
      schemaVersion: 1,
      result: "FAIL",
      reason: "adaptive_empty_output",
      exit_code: cp.status,
    };
  }
  try {
    const parsed = JSON.parse(cp.stdout) as AdaptiveResult;
    const result = parsed.result;
    if (typeof result !== "string") {
      return {
        schemaVersion: 1,
        result: "FAIL",
        reason: "adaptive_result_missing",
        exit_code: cp.status,
      };
    }
    const successResult = result === "PASS" || result === "CONDITIONAL";
    if (cp.status !== 0 && successResult) {
      return {
        schemaVersion: 1,
        result: "FAIL",
        reason: "adaptive_exit_result_mismatch",
        child_result: result,
        exit_code: cp.status,
      };
    }
    return parsed;
  } catch {
    return {
      schemaVersion: 1,
      result: "FAIL",
      reason: "adaptive_non_json_output",
      exit_code: cp.status,
    };
  }
}

export function runCapabilityHealth(): AdaptiveResult {
  return runFixedScript(HEALTH_SCRIPT, ["cached"]);
}

export function runCapabilityRoute(input: {
  intent: string;
  needsWrite?: boolean;
  preferLocal?: boolean;
  requireReady?: boolean;
}): AdaptiveResult {
  const args = ["--intent", input.intent];
  if (input.needsWrite) args.push("--needs-write");
  if (input.preferLocal) args.push("--prefer-local");
  if (input.requireReady) args.push("--require-ready");
  return runFixedScript(ROUTER_SCRIPT, args);
}
