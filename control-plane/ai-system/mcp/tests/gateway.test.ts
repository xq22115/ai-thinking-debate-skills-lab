import assert from "node:assert/strict";
import test from "node:test";
import { Client, StreamableHTTPClientTransport } from "@modelcontextprotocol/client";

import { createGatewayHandler } from "../src/mcp.js";

test("gateway lists read-only tools and calls capability/preflight tools", async () => {
  process.env.ORDINARY_CHAT_MCP_ALLOW_SUBMIT = "false";
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
    const listed = await client.listTools();
    const names = listed.tools.map((tool) => tool.name).sort();
    assert.deepEqual(names, [
      "agent_receipt_summary",
      "agent_run_status",
      "bridge_preflight",
      "capabilities",
    ]);

    const capabilities = await client.callTool({ name: "capabilities", arguments: {} });
    const capabilityData = capabilities.structuredContent as Record<string, unknown>;
    assert.equal(capabilityData.schemaVersion, 1);
    assert.ok(Array.isArray(capabilityData.capabilities));

    const preflight = await client.callTool({ name: "bridge_preflight", arguments: {} });
    const preflightData = preflight.structuredContent as Record<string, unknown>;
    assert.equal(preflightData.result, "BLOCKED");
    assert.equal(preflightData.allowed_roots_configured, false);
  } finally {
    await client.close();
    await handler.close();
  }
});
