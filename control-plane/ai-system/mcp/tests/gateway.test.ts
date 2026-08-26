import assert from "node:assert/strict";
import test from "node:test";
import { Client, StreamableHTTPClientTransport } from "@modelcontextprotocol/client";

import { createGatewayHandler } from "../src/mcp.js";

const DEFAULT_READ_ONLY_TOOLS = [
  "agent_receipt_summary",
  "agent_run_liveness",
  "agent_run_status",
  "bridge_preflight",
  "capabilities",
  "capability_health",
  "capability_route",
  "project_memory_search",
].sort();

test("gateway exposes only the expected read-only default surface in the modern MCP era", async () => {
  process.env.ORDINARY_CHAT_MCP_ALLOW_SUBMIT = "false";
  process.env.ORDINARY_CHAT_MEMORY_ALLOW_WRITE = "false";
  delete process.env.ORDINARY_CHAT_ALLOWED_ROOTS;

  const handler = createGatewayHandler();
  const transport = new StreamableHTTPClientTransport(new URL("http://test.local/mcp"), {
    fetch: (url, init) => handler.fetch(new Request(url, init)),
  });
  const client = new Client(
    { name: "ordinary-chat-gateway-test", version: "1.0.0" },
    { versionNegotiation: { mode: "auto" } },
  );

  try {
    await client.connect(transport);
    assert.equal(client.getProtocolEra(), "modern", "gateway must negotiate the 2026-era MCP wire protocol");

    const listed = await client.listTools();
    const names = listed.tools.map((tool) => tool.name).sort();
    assert.deepEqual(names, DEFAULT_READ_ONLY_TOOLS);
    assert.equal(names.includes("agent_submit_chat_work"), false);
    assert.equal(names.includes("agent_submit_a01_a10"), false);
    assert.equal(names.includes("project_memory_add"), false);
    assert.equal(names.includes("project_memory_delete"), false);

    for (const tool of listed.tools) {
      assert.equal(tool.annotations?.readOnlyHint, true, `${tool.name} must be read-only by default`);
      assert.equal(tool.annotations?.destructiveHint, false, `${tool.name} must not be destructive`);
    }

    const capabilities = await client.callTool({ name: "capabilities", arguments: {} });
    const capabilityData = capabilities.structuredContent as Record<string, unknown>;
    assert.equal(capabilityData.schemaVersion, 1);
    assert.ok(Array.isArray(capabilityData.capabilities));

    const health = await client.callTool({ name: "capability_health", arguments: {} });
    const healthData = health.structuredContent as Record<string, unknown>;
    assert.equal(healthData.result, "PASS");
    assert.equal(healthData.schemaVersion, 1);
    assert.equal(typeof healthData.capabilities, "object");

    const route = await client.callTool({
      name: "capability_route",
      arguments: { intent: "repository_action" },
    });
    const routeData = route.structuredContent as Record<string, unknown>;
    assert.equal(routeData.result, "CONDITIONAL");
    const selected = routeData.selected as Record<string, unknown>;
    assert.equal(selected.id, "github-native");

    const readyOnlyRoute = await client.callTool({
      name: "capability_route",
      arguments: { intent: "repository_action", requireReady: true },
    });
    const readyOnlyData = readyOnlyRoute.structuredContent as Record<string, unknown>;
    assert.equal(readyOnlyData.result, "BLOCKED");
    assert.equal(readyOnlyData.reason, "no_compatible_ready_route");

    const preflight = await client.callTool({ name: "bridge_preflight", arguments: {} });
    const preflightData = preflight.structuredContent as Record<string, unknown>;
    assert.equal(preflightData.result, "BLOCKED");
    assert.equal(preflightData.allowed_roots_configured, false);

    const liveness = await client.callTool({
      name: "agent_run_liveness",
      arguments: { runId: "f".repeat(32) },
    });
    const livenessData = liveness.structuredContent as Record<string, unknown>;
    assert.equal(livenessData.result, "NOT_FOUND");
    assert.equal(livenessData.schemaVersion, 2);
  } finally {
    await client.close();
    await handler.close();
  }
});

test("transport interruption fails closed and a fresh modern-era client reconnects", async () => {
  process.env.ORDINARY_CHAT_MCP_ALLOW_SUBMIT = "false";
  process.env.ORDINARY_CHAT_MEMORY_ALLOW_WRITE = "false";
  delete process.env.ORDINARY_CHAT_ALLOWED_ROOTS;

  const handler = createGatewayHandler();
  let disconnected = false;
  const makeTransport = () =>
    new StreamableHTTPClientTransport(new URL("http://test.local/mcp"), {
      fetch: async (url, init) => {
        if (disconnected) {
          throw new TypeError("simulated MCP transport interruption");
        }
        return handler.fetch(new Request(url, init));
      },
    });

  const first = new Client(
    { name: "ordinary-chat-chaos-client-1", version: "1.0.0" },
    { versionNegotiation: { mode: "auto" } },
  );
  let second: Client | null = null;

  try {
    await first.connect(makeTransport());
    assert.equal(first.getProtocolEra(), "modern", "initial client must negotiate the modern MCP era");
    const before = await first.listTools();
    assert.deepEqual(before.tools.map((tool) => tool.name).sort(), DEFAULT_READ_ONLY_TOOLS);

    disconnected = true;
    await assert.rejects(
      first.listTools(),
      (error: unknown) => error instanceof TypeError && error.message.includes("simulated MCP transport interruption"),
    );

    // Recovery is explicit: restore the transport and establish a fresh client.
    // No cached tool-list response is accepted as proof that the disconnected
    // session remained healthy.
    disconnected = false;
    await first.close();
    second = new Client(
      { name: "ordinary-chat-chaos-client-2", version: "1.0.0" },
      { versionNegotiation: { mode: "auto" } },
    );
    await second.connect(makeTransport());
    assert.equal(second.getProtocolEra(), "modern", "reconnected client must negotiate the modern MCP era");
    const after = await second.listTools();
    assert.deepEqual(after.tools.map((tool) => tool.name).sort(), DEFAULT_READ_ONLY_TOOLS);
  } finally {
    disconnected = false;
    if (second) {
      await second.close();
    } else {
      try {
        await first.close();
      } catch {
        // The primary assertion above already verifies the interruption path.
      }
    }
    await handler.close();
  }
});
