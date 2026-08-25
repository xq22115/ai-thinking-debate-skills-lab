import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_MEMORY = path.resolve(HERE, "../../../scripts/project_memory.py");

function scriptPath(): string {
  return process.env.ORDINARY_CHAT_MEMORY_SCRIPT?.trim() || DEFAULT_MEMORY;
}

export function memoryWriteEnabled(): boolean {
  return process.env.ORDINARY_CHAT_MEMORY_ALLOW_WRITE === "true";
}

export function runMemory(args: string[], stdin?: string): Record<string, unknown> {
  const script = scriptPath();
  if (!fs.existsSync(script)) {
    return { schemaVersion: 1, result: "BLOCKED", reason: "memory_script_missing" };
  }
  const cp = spawnSync(process.env.PYTHON_BIN?.trim() || "python3", [script, ...args], {
    input: stdin,
    encoding: "utf8",
    timeout: 15000,
    maxBuffer: 2 * 1024 * 1024,
    env: process.env,
  });
  if (cp.error) {
    return { schemaVersion: 1, result: "BLOCKED", reason: `memory_spawn_error:${cp.error.name}` };
  }
  try {
    return JSON.parse(cp.stdout || "{}") as Record<string, unknown>;
  } catch {
    return { schemaVersion: 1, result: "FAIL", reason: "memory_non_json_output", exit_code: cp.status };
  }
}
