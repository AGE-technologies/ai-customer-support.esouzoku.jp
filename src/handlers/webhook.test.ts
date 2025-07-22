import { assertEquals } from "https://deno.land/std@0.208.0/assert/mod.ts";
import { createApp } from "../server.ts";
import type { HubSpotWebhookPayload } from "../types/index.ts";

Deno.test("POST /webhook/hubspot processes ticket creation", async () => {
  const app = createApp();

  const mockPayload: HubSpotWebhookPayload = {
    eventId: "test-event-123",
    subscriptionId: 12345,
    portalId: 67890,
    occurredAt: Date.now(),
    subscriptionType: "ticket.creation",
    attemptNumber: 0,
    objectId: 111222,
    changeSource: "CRM_UI",
    changeFlag: "NEW",
    objectTypeId: "0-5",
  };

  const req = new Request("http://localhost/webhook/hubspot", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(mockPayload),
  });

  const res = await app.request(req);

  assertEquals(res.status, 200);
  const response = await res.json();
  assertEquals(response.status, "received");
  assertEquals(response.eventId, "test-event-123");
});

Deno.test("POST /webhook/hubspot returns 400 for invalid payload", async () => {
  const app = createApp();

  const req = new Request("http://localhost/webhook/hubspot", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ invalid: "payload" }),
  });

  const res = await app.request(req);

  assertEquals(res.status, 400);
  const response = await res.json();
  assertEquals(response.error, "Invalid webhook payload");
});
