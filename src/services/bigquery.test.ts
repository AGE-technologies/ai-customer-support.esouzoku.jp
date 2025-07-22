import { assertEquals } from "https://deno.land/std@0.208.0/assert/mod.ts";
import { BigQueryService } from "./bigquery.ts";

Deno.test("BigQueryService extracts Q&A pairs", async () => {
  const service = new BigQueryService({
    projectId: "test-project",
  });

  const qaPairs = await service.extractQAPairs("2024-01-01");

  assertEquals(qaPairs.length, 1);
  assertEquals(qaPairs[0].thread_id, "mock-thread-1");
  assertEquals(typeof qaPairs[0].query, "string");
  assertEquals(typeof qaPairs[0].response, "string");
  assertEquals(typeof qaPairs[0].metadata.query_id, "string");
  assertEquals(typeof qaPairs[0].metadata.response_id, "string");
});

Deno.test("BigQueryService loads SQL query from file", async () => {
  const service = new BigQueryService({
    projectId: "test-project",
  });

  // Test that the SQL file can be loaded and processed
  const qaPairs = await service.extractQAPairs("2024-06-01");
  
  assertEquals(qaPairs.length >= 1, true);
});