import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export type BridgeResult = Record<string, unknown>;

const HERE = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_BRIDGE = path.resolve(HERE, "../../../scripts/ordinary_chat_bridge.py");
const CAPABILITY_FILE = path.resolve(HERE, "../../configs/ordinary-chat-capabilities.json");

function pythonBin(): string {
  return process.env.PYTHON_BIN?.trim() || "python3";
}

function boundedTimeout(raw: string | undefined, fallback: number): number {
  const parsed = Number(raw ?? fallback);
  return Number.isFinite(parsed) && parsed >= 100 && parsed <= 120_000 ? parsed : fallback;
}

export function bridgePath(): string {
  return process.env.ORDINARY_CHAT_BRIDGE_PATH?.trim() || DEFAULT_BRIDGE;
}

export function bridgePresent(): boolean {
  try {
    return fs.statSync(bridgePath()).isFile();
  } catch {
    return false;
  }
}

export function readCapabilities(): BridgeResult {
  try {
    const parsed = JSON.parse(fs.readFileSync(CAPABILITY_FILE, "utf8")) as BridgeResult;
    if (!Array.isArray(parsed.capabilities)) {
      throw new Error("capabilities_not_array");
    }
    return parsed;
  } catch (error) {
    return {
      schemaVersion: 1,
      capabilities: [],
      result: "FAIL",
      reason: `capability_registry_unavailable:${error instanceof Error ? error.name : "unknown"}`,
    };
  }
}

export function runBridge(args: string[], stdin?: string): BridgeResult {
  if (!bridgePresent()) {
    return { schemaVersion: 1, result: "BLOCKED", reason: "bridge_script_missing" };
  }
  const cp = spawnSync(pythonBin(), [bridgePath(), ...args], {
    input: stdin,
    encoding: "utf8",
    timeout: boundedTimeout(process.env.ORDINARY_CHAT_BRIDGE_TIMEOUT_MS, 15_000),
    maxBuffer: 2 * 1024 * 1024,
    env: process.env,
  });
  if (cp.error) {
    return {
      schemaVersion: 1,
      result: "BLOCKED",
      reason: `bridge_spawn_error:${cp.error.name}`,
      signal: cp.signal,
    };
  }
  if (!cp.stdout?.trim()) {
    return {
      schemaVersion: 1,
      result: "FAIL",
      reason: "bridge_empty_output",
      exit_code: cp.status,
      signal: cp.signal,
    };
  }
  try {
    const parsed = JSON.parse(cp.stdout) as BridgeResult;
    if (typeof parsed.result !== "string" && typeof parsed.status !== "string") {
      return {
        schemaVersion: 1,
        result: "FAIL",
        reason: "bridge_result_missing_status",
        exit_code: cp.status,
      };
    }
    const successLike = new Set(["PASS", "QUEUED", "RUNNING"]);
    const reported = String(parsed.result ?? parsed.status ?? "");
    if (cp.status !== 0 && successLike.has(reported)) {
      return {
        schemaVersion: 1,
        result: "FAIL",
        reason: "bridge_exit_status_mismatch",
        reported_result: reported,
        exit_code: cp.status,
      };
    }
    if (cp.status !== null) parsed.exit_code = cp.status;
    return parsed;
  } catch {
    return {
      schemaVersion: 1,
      result: "FAIL",
      reason: "bridge_non_json_output",
      exit_code: cp.status,
      signal: cp.signal,
    };
  }
}

export function submitEnabled(): boolean {
  return process.env.ORDINARY_CHAT_MCP_ALLOW_SUBMIT === "true";
}
