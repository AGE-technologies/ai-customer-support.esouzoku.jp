import type { QAPair } from "../types/index.ts";

export interface BigQueryConfig {
  projectId: string;
  keyFilename?: string;
}

export class BigQueryService {
  private config: BigQueryConfig;

  constructor(config: BigQueryConfig) {
    this.config = config;
  }

  async extractQAPairs(startDate: string = "2024-01-01"): Promise<QAPair[]> {
    const queryPath = new URL("../queries/extract-qa-pairs.sql", import.meta.url);
    const queryText = await Deno.readTextFile(queryPath);
    
    const query = queryText.replace("@start_date", `'${startDate}'`);
    
    // For now, return mock data during development
    // TODO: Implement actual BigQuery client connection
    console.log(`Would execute BigQuery with start_date: ${startDate}`);
    console.log("Query preview:", query.substring(0, 200) + "...");
    
    return [
      {
        thread_id: "mock-thread-1",
        timestamp: new Date().toISOString(),
        query: "サンプル質問：相続登記について教えてください",
        response: "サンプル回答：相続登記は...",
        metadata: {
          query_id: "mock-q1",
          response_id: "mock-r1",
          query_time: new Date().toISOString(),
          response_time: new Date().toISOString(),
          response_delay_days: 0,
        },
      },
    ];
  }

  async executeQuery(query: string): Promise<unknown[]> {
    // TODO: Implement actual BigQuery execution
    console.log("Executing query:", query.substring(0, 100) + "...");
    throw new Error("BigQuery client not implemented yet");
  }
}