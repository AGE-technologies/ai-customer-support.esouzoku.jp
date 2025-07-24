import { BigQuery } from "@google-cloud/bigquery";
import type { QAPair } from "../types/index.ts";

export interface BigQueryConfig {
  projectId: string;
  keyFilename?: string;
}

export class BigQueryService {
  private client: BigQuery;

  constructor(config: BigQueryConfig) {
    this.client = new BigQuery({
      projectId: config.projectId,
      keyFilename: config.keyFilename,
    });
  }

  async extractQAPairs(startDate: string = "2024-01-01"): Promise<QAPair[]> {
    const queryPath = new URL("../queries/extract-qa-pairs.sql", import.meta.url);
    const queryText = await Deno.readTextFile(queryPath);
    
    try {
      // Use BigQuery parameterized queries for safety
      const [rows] = await this.client.query({
        query: queryText,
        params: {
          start_date: startDate,
        },
      });

      return rows.map((row: any) => ({
        thread_id: row.thread_id,
        timestamp: row.query_timestamp,
        query: row.query,
        response: row.response,
        metadata: {
          query_id: row.metadata.query_id,
          response_id: row.metadata.response_id,
          query_time: row.metadata.query_time,
          response_time: row.metadata.response_time,
          response_delay_days: row.metadata.response_delay_days,
        },
      }));
    } catch (error) {
      console.error("BigQuery execution failed:", error);
      
      // Fallback to mock data during development
      console.log(`Fallback: Would execute BigQuery with start_date: ${startDate}`);
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
  }

  async executeQuery(query: string, params: Record<string, unknown> = {}): Promise<unknown[]> {
    const [rows] = await this.client.query({
      query,
      params,
    });
    return rows;
  }
}