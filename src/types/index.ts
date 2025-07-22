export interface HubSpotWebhookPayload {
  eventId: string;
  subscriptionId: number;
  portalId: number;
  occurredAt: number;
  subscriptionType: string;
  attemptNumber: number;
  objectId: number;
  changeSource: string;
  changeFlag: string;
  objectTypeId: string;
  propertyName?: string;
  propertyValue?: string;
}

export interface CustomerInquiry {
  id: string;
  content: string;
  email: string;
  timestamp: Date;
  hubspotContactId?: number;
  hubspotTicketId?: number;
}

export interface RAGResponse {
  answer: string;
  confidence: number;
  sources: Array<{
    id: string;
    content: string;
    similarity: number;
  }>;
}
