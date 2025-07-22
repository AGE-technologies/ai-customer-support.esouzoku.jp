import type { Context } from "hono";
import type { HubSpotWebhookPayload } from "../types/index.ts";

export function validateWebhookPayload(
  payload: unknown,
): payload is HubSpotWebhookPayload {
  if (!payload || typeof payload !== "object") return false;

  const p = payload as Record<string, unknown>;

  return (
    typeof p.eventId === "string" &&
    typeof p.subscriptionId === "number" &&
    typeof p.portalId === "number" &&
    typeof p.occurredAt === "number" &&
    typeof p.subscriptionType === "string" &&
    typeof p.attemptNumber === "number" &&
    typeof p.objectId === "number" &&
    typeof p.changeSource === "string" &&
    typeof p.changeFlag === "string" &&
    typeof p.objectTypeId === "string"
  );
}

export async function handleHubSpotWebhook(c: Context) {
  try {
    const payload = await c.req.json();

    if (!validateWebhookPayload(payload)) {
      return c.json({ error: "Invalid webhook payload" }, 400);
    }

    console.log(
      `Received HubSpot webhook: ${payload.subscriptionType} for object ${payload.objectId}`,
    );

    return c.json({
      status: "received",
      eventId: payload.eventId,
    });
  } catch (error) {
    console.error("Error processing webhook:", error);
    return c.json({ error: "Internal server error" }, 500);
  }
}
