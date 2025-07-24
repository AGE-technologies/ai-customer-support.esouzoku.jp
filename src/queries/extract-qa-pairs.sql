-- Q&A pair extraction query for RAG training data
-- Extracts customer questions and support responses from HubSpot data
-- Groups by thread_id to ensure proper conversation context
-- BigQuery parameters: @start_date (e.g., '2024-01-01')

WITH thread_timeline AS (
    -- チケット（フォーム送信など）
    SELECT
        CAST(hs_auto_generated_from_thread_id AS STRING) AS thread_id,
        CAST(id AS STRING) AS message_id,
        'ticket' AS message_type,
        DATETIME(TIMESTAMP(createdat), 'Asia/Tokyo') AS created_at,
        content AS message_content,
        'INBOUND' AS direction
    FROM bronze_hubspot.tickets_with_literal_props
    WHERE
        hs_auto_generated_from_thread_id IS NOT NULL
        AND content IS NOT NULL
        AND LENGTH(content) > 20
        AND createdat >= @start_date

    UNION ALL

    -- メール履歴
    SELECT
        hs_email_thread_id AS thread_id,
        id AS message_id,
        'email' AS message_type,
        DATETIME(TIMESTAMP(createdat), 'Asia/Tokyo') AS created_at,
        hs_body_preview AS message_content,
        CASE
            WHEN
                hs_email_from_email LIKE '%age-technologies.co.jp'
                OR hs_email_from_email LIKE '%so-zo-ku.com'
                THEN 'OUTBOUND'
            ELSE 'INBOUND'
        END AS direction
    FROM bronze_hubspot.engagements_emails_with_literal_props
    WHERE
        hs_email_thread_id IS NOT NULL
        AND hs_body_preview IS NOT NULL
        AND LENGTH(hs_body_preview) > 20
        AND createdat >= @start_date
),

qa_candidates AS (
    SELECT
        thread_id,
        message_id,
        created_at,
        SUBSTR(message_content, 1, 1000) AS message_content,
        direction,
        LEAD(message_id) OVER (
            PARTITION BY thread_id
            ORDER BY created_at
        ) AS next_message_id,
        LEAD(direction) OVER (
            PARTITION BY thread_id
            ORDER BY created_at
        ) AS next_direction,
        LEAD(SUBSTR(message_content, 1, 1000)) OVER (
            PARTITION BY thread_id
            ORDER BY created_at
        ) AS next_message_content,
        LEAD(created_at) OVER (
            PARTITION BY thread_id
            ORDER BY created_at
        ) AS next_created_at
    FROM thread_timeline
)

SELECT
    thread_id,
    created_at AS query_timestamp,
    message_content AS query,
    next_message_content AS response,
    STRUCT(
        message_id AS query_id,
        next_message_id AS response_id,
        created_at AS query_time,
        next_created_at AS response_time,
        DATE_DIFF(DATE(next_created_at), DATE(created_at), DAY) AS response_delay_days
    ) AS metadata
FROM qa_candidates
WHERE
    direction = 'INBOUND'
    AND next_direction = 'OUTBOUND'
    AND DATE_DIFF(DATE(next_created_at), DATE(created_at), DAY) <= 7
ORDER BY created_at DESC
