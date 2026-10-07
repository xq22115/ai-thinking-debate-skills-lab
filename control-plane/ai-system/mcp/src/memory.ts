import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_MEMORY = path.resolve(HERE, "../../../scripts/project_memory.py");

function scriptPath(): string {
  return process.env.ORDINARY_CHAT_MEMORY_SCRIPT?.trim() || DEFAULT_MEMORY;
}

function boundedTimeout(raw: string | undefined, fallback: number): number {
  const parsed = Number(raw ?? fallback);
  return Number.isFinite(parsed) && parsed >= 100 && parsed <= 120_000 ? parsed : fallback;
}

export function memoryWriteEnabled(): boolean {
  return process.env.ORDINARY_CHAT_MEMORY_ALLOW_WRITE === "true";
}

export function runMemory(args: string[], stdin?: string): Record<string, unknown> {
  const script = scriptPath();
  try {
    if (!fs.statSync(script).isFile()) {
      return { schemaVersion: 1, result: "BLOCKED", reason: "memory_script_missing" };
    }
  } catch {
    return { schemaVersion: 1, result: "BLOCKED", reason: "memory_script_missing" };
  }
  const cp = spawnSync(process.env.PYTHON_BIN?.trim() || "python3", [script, ...args], {
    input: stdin,
    encoding: "utf8",
    timeout: boundedTimeout(process.env.ORDINARY_CHAT_MEMORY_TIMEOUT_MS, 15_000),
    maxBuffer: 2 * 1024 * 1024,
    env: process.env,
  });
  if (cp.error) {
    return {
      schemaVersion: 1,
      result: "BLOCKED",
      reason: `memory_spawn_error:${cp.error.name}`,
      signal: cp.signal,
    };
  }
  if (!cp.stdout?.trim()) {
    return {
      schemaVersion: 1,
      result: "FAIL",
      reason: "memory_empty_output",
      exit_code: cp.status,
      signal: cp.signal,
    };
  }
  try {
    const parsed = JSON.parse(cp.stdout) as Record<string, unknown>;
    if (typeof parsed.result !== "string") {
      return {
        schemaVersion: 1,
        result: "FAIL",
        reason: "memory_result_missing_status",
        exit_code: cp.status,
      };
    }
    if (cp.status !== 0 && parsed.result === "PASS") {
      return {
        schemaVersion: 1,
        result: "FAIL",
        reason: "memory_exit_status_mismatch",
        exit_code: cp.status,
      };
    }
    if (cp.status !== null) parsed.exit_code = cp.status;
    return parsed;
  } catch {
    return {
      schemaVersion: 1,
      result: "FAIL",
      reason: "memory_non_json_output",
      exit_code: cp.status,
      signal: cp.signal,
    };
  }
}
