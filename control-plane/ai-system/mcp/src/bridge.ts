import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export type BridgeResult = Record<string, unknown>;

const HERE = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_BRIDGE = path.resolve(HERE, "../../../scripts/ordinary_chat_bridge.py");
const CAPABILITY_FILE = path.resolve(
  HERE,
  "../../configs/ordinary-chat-capabilities.json",
);

function pythonBin(): string {
  return process.env.PYTHON_BIN?.trim() || "python3";
}

export function bridgePath(): string {
  return process.env.ORDINARY_CHAT_BRIDGE_PATH?.trim() || DEFAULT_BRIDGE;
}

export function bridgePresent(): boolean {
  return fs.existsSync(bridgePath());
}

export function readCapabilities(): BridgeResult {
  try {
    return JSON.parse(fs.readFileSync(CAPABILITY_FILE, "utf8")) as BridgeResult;
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
  const timeout = Number(process.env.ORDINARY_CHAT_BRIDGE_TIMEOUT_MS ?? 15000);
  const cp = spawnSync(pythonBin(), [bridgePath(), ...args], {
    input: stdin,
    encoding: "utf8",
    timeout: Number.isFinite(timeout) ? timeout : 15000,
    maxBuffer: 2 * 1024 * 1024,
    env: process.env,
  });
  if (cp.error) {
    return {
      schemaVersion: 1,
      result: "BLOCKED",
      reason: `bridge_spawn_error:${cp.error.name}`,
    };
  }
  try {
    const parsed = JSON.parse(cp.stdout || "{}") as BridgeResult;
    if (cp.status !== 0 && !parsed.result) {
      parsed.result = "BLOCKED";
    }
    return parsed;
  } catch {
    return {
      schemaVersion: 1,
      result: "FAIL",
      reason: "bridge_non_json_output",
      exit_code: cp.status,
    };
  }
}

export function submitEnabled(): boolean {
  return process.env.ORDINARY_CHAT_MCP_ALLOW_SUBMIT === "true";
}
