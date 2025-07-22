-- Q&A pair extraction query for RAG training data
-- Extracts customer questions and support responses from HubSpot data
-- Groups by thread_id to ensure proper conversation context

WITH thread_timeline AS (
  -- チケット（フォーム送信など）
  SELECT 
    CAST(hs_auto_generated_from_thread_id AS STRING) as thread_id,
    CAST(id AS STRING) as message_id,
    'ticket' as message_type,
    DATETIME(TIMESTAMP(createdAt), 'Asia/Tokyo') as created_at,
    content as message_content,
    'INBOUND' as direction
  FROM bronze_hubspot.tickets_with_literal_props 
  WHERE hs_auto_generated_from_thread_id IS NOT NULL 
    AND content IS NOT NULL 
    AND LENGTH(content) > 20
    AND createdAt >= @start_date
  
  UNION ALL
  
  -- メール履歴
  SELECT 
    hs_email_thread_id as thread_id,
    id as message_id,
    'email' as message_type,
    DATETIME(TIMESTAMP(createdAt), 'Asia/Tokyo') as created_at,
    hs_body_preview as message_content,
    CASE WHEN hs_email_from_email LIKE '%age-technologies.co.jp' 
              OR hs_email_from_email LIKE '%so-zo-ku.com' 
         THEN 'OUTBOUND' ELSE 'INBOUND' END as direction
  FROM bronze_hubspot.engagements_emails_with_literal_props 
  WHERE hs_email_thread_id IS NOT NULL 
    AND hs_body_preview IS NOT NULL 
    AND LENGTH(hs_body_preview) > 20
    AND createdAt >= @start_date
),
qa_candidates AS (
  SELECT 
    thread_id,
    message_id,
    created_at,
    SUBSTR(message_content, 1, 1000) as message_content,
    direction,
    LEAD(message_id) OVER (PARTITION BY thread_id ORDER BY created_at) as next_message_id,
    LEAD(direction) OVER (PARTITION BY thread_id ORDER BY created_at) as next_direction,
    LEAD(SUBSTR(message_content, 1, 1000)) OVER (PARTITION BY thread_id ORDER BY created_at) as next_message_content,
    LEAD(created_at) OVER (PARTITION BY thread_id ORDER BY created_at) as next_created_at
  FROM thread_timeline
)
SELECT
  thread_id,
  created_at as timestamp,
  message_content as query,
  next_message_content as response,
  STRUCT(
    message_id as query_id,
    next_message_id as response_id,
    created_at as query_time,
    next_created_at as response_time,
    DATE_DIFF(DATE(next_created_at), DATE(created_at), DAY) as response_delay_days
  ) as metadata
FROM qa_candidates
WHERE direction = 'INBOUND' 
  AND next_direction = 'OUTBOUND'
  AND DATE_DIFF(DATE(next_created_at), DATE(created_at), DAY) <= 7
ORDER BY created_at DESC