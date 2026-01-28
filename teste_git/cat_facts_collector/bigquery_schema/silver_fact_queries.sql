/*
 * Silver layer - Cat Facts (SQL snippets)
 *
 * Arquivo: silver_fact_queries.sql
 * Objetivo: Conjunto de consultas úteis para a tabela SILVER (fato tratado/limpo)
 * Instruções: substitua `project-id.dataset` pelos seus valores reais.
 * Autor: Data Engineering Team
 * Data: 2026-01-27
 */

-- 1) UPSERT (MERGE) do Bronze para a Silver
-- Mantém registros atualizados por `fact_id`, atualiza quando `updated_at` for mais recente.
MERGE `project-id.dataset.silver_cat_facts` T
USING (
  SELECT * FROM `project-id.dataset.bronze_cat_facts`
  WHERE record_status = 'active'
) S
ON T.fact_id = S.id
WHEN MATCHED AND S.updated_at > T.updated_at THEN
  UPDATE SET
    text = S.text,
    text_length = LENGTH(S.text),
    status = S.status,
    user_id = S.user_id,
    verification_level = S.verification.level,
    updated_at = S.updated_at,
    ingestion_timestamp = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN
  INSERT (fact_id, text, text_length, status, user_id, verification_level, created_at, updated_at, ingestion_timestamp, record_status)
  VALUES (S.id, S.text, LENGTH(S.text), S.status, S.user_id, S.verification.level, S.created_at, S.updated_at, CURRENT_TIMESTAMP(), S.record_status);


-- 2) Consulta de amostra limpa da SILVER (preview)
SELECT
  fact_id,
  text,
  text_length,
  created_at,
  updated_at,
  status,
  verification_level
FROM
  `project-id.dataset.silver_cat_facts`
WHERE
  record_status = 'active'
ORDER BY
  updated_at DESC
LIMIT 100;


-- 3) Checagens de qualidade: contagens de NULLs e percentuais
SELECT
  COUNT(*) AS total_registros,
  SUM(CASE WHEN text IS NULL OR text = '' THEN 1 ELSE 0 END) AS text_missing,
  ROUND(100 * SUM(CASE WHEN text IS NULL OR text = '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct_text_missing,
  SUM(CASE WHEN SAFE_CAST(created_at AS TIMESTAMP) IS NULL THEN 1 ELSE 0 END) AS created_at_invalid,
  SUM(CASE WHEN SAFE_CAST(updated_at AS TIMESTAMP) IS NULL THEN 1 ELSE 0 END) AS updated_at_invalid,
  SUM(CASE WHEN LENGTH(text) > 10000 THEN 1 ELSE 0 END) AS very_long_texts
FROM
  `project-id.dataset.silver_cat_facts`
WHERE
  record_status = 'active';


-- 4) Duplicidade por ID (deve ser 0)
SELECT
  fact_id,
  COUNT(*) AS cnt
FROM
  `project-id.dataset.silver_cat_facts`
GROUP BY fact_id
HAVING COUNT(*) > 1
ORDER BY cnt DESC
LIMIT 50;


-- 5) Regras de transformação: exemplo de normalização de texto (trim + collapsing spaces)
SELECT
  fact_id,
  REGEXP_REPLACE(TRIM(text), r"\s+", ' ') AS text_normalized,
  LOWER(REGEXP_REPLACE(TRIM(text), r"\s+", ' ')) AS text_normalized_lower
FROM
  `project-id.dataset.silver_cat_facts`
WHERE
  record_status = 'active'
LIMIT 100;


-- 6) Última atualização por fonte (contagem e última data)
SELECT
  s.api_source AS source_name,
  COUNT(f.fact_id) AS total_facts,
  MAX(f.updated_at) AS last_update
FROM
  `project-id.dataset.silver_cat_facts` f
LEFT JOIN
  `project-id.dataset.dim_source` s
ON f.source_sk = s.source_sk
WHERE
  f.record_status = 'active'
GROUP BY s.api_source
ORDER BY total_facts DESC;


-- 7) Tendência diária de novos/atualizados (últimos 30 dias)
SELECT
  DATE(updated_at) AS day,
  COUNT(*) AS total_updates
FROM
  `project-id.dataset.silver_cat_facts`
WHERE
  updated_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  AND record_status = 'active'
GROUP BY day
ORDER BY day DESC;


-- 8) Anomalias: textos com possíveis quebras de linha ou control chars
SELECT
  fact_id,
  text,
  REGEXP_CONTAINS(text, r"[\r\n]") AS has_newline,
  REGEXP_CONTAINS(text, r"[\x00-\x08\x0B\x0C\x0E-\x1F]") AS has_control_chars
FROM
  `project-id.dataset.silver_cat_facts`
WHERE
  record_status = 'active'
  AND (REGEXP_CONTAINS(text, r"[\r\n]") OR REGEXP_CONTAINS(text, r"[\x00-\x08\x0B\x0C\x0E-\x1F]"))
LIMIT 200;


-- 9) Amostra estratificada por fonte (10% por fonte)
WITH source_counts AS (
  SELECT source_sk, COUNT(*) AS total
  FROM `project-id.dataset.silver_cat_facts`
  WHERE record_status = 'active'
  GROUP BY source_sk
),
ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY source_sk ORDER BY RAND()) AS rn
  FROM `project-id.dataset.silver_cat_facts`
  WHERE record_status = 'active'
)
SELECT r.fact_id, r.text, r.created_at, r.updated_at, r.source_sk
FROM ranked r
JOIN source_counts sc ON r.source_sk = sc.source_sk
WHERE r.rn <= CAST(sc.total * 0.1 AS INT64)
ORDER BY r.source_sk, r.rn
LIMIT 10000;


-- 10) Recomendações (comentadas):
-- - Particionar `silver_cat_facts` por DATE(updated_at) para consultas de janela temporal.
-- - Cluster por source_sk, status para acelerar filtros por fonte/status.
-- - Rodar checagens de qualidade (query 3) diariamente via scheduled query.

-- FIM
