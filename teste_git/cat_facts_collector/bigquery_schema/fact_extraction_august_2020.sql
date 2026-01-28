/*
 * Questão 4 - UOLCatLovers Case Study
 * 
 * Objetivo: Extrair fatos sobre gatos que foram atualizados em agosto de 2020
 * 
 * Descrição:
 * Esta query busca todos os cat facts que tiveram updated_at em agosto/2020,
 * trazendo informações completas do modelo dimensional (fact + dimensions).
 * 
 * Modelo: Star Schema (fact_cat_facts + dimensões)
 * Autor: Data Engineering Team
 * Data: 2026-01-27
 */

-- Query 1: Versão simples - Apenas da tabela FATO
SELECT 
    fact_id,
    text,
    updated_at,
    status,
    user_id,
    verification_level,
    record_status,
    ingestion_timestamp,
    last_update_timestamp
FROM 
    `project-id.dataset.fact_cat_facts`
WHERE 
    -- Filtra atualizações de agosto de 2020
    EXTRACT(YEAR FROM updated_at) = 2020
    AND EXTRACT(MONTH FROM updated_at) = 8
    AND record_status = 'active'  -- Apenas registros ativos
ORDER BY 
    updated_at DESC;


-- Query 2: Versão completa - Com todas as dimensões (Star Schema)
SELECT 
    -- Campos da FATO
    f.fact_id,
    f.text,
    f.text_length,
    f.updated_at,
    f.status,
    f.user_id,
    f.verification_level,
    f.record_status,
    
    -- Dimensão SOURCE
    s.api_source,
    s.api_version,
    s.extraction_method,
    
    -- Dimensão DATE (data de atualização)
    d.full_date,
    d.day_of_week,
    d.day_of_week_name,
    d.week_of_year,
    d.month_number,
    d.month_name,
    d.quarter,
    d.year,
    d.is_weekend,
    
    -- Dimensão TIME (hora de ingestão)
    t.hour,
    t.minute,
    t.time_of_day_period,
    
    -- Dimensão QUALITY
    q.quality_score,
    q.data_completeness_pct,
    q.has_validation_errors,
    q.validation_error_count,
    
    -- Timestamps de controle
    f.ingestion_timestamp,
    f.last_update_timestamp

FROM 
    `project-id.dataset.fact_cat_facts` f
    
    -- JOIN com dimensão SOURCE
    LEFT JOIN `project-id.dataset.dim_source` s
        ON f.source_sk = s.source_sk
    
    -- JOIN com dimensão DATE (usando data de atualização)
    LEFT JOIN `project-id.dataset.dim_date` d
        ON DATE(f.updated_at) = d.full_date
    
    -- JOIN com dimensão TIME (usando horário de ingestão)
    LEFT JOIN `project-id.dataset.dim_time` t
        ON f.ingestion_time_sk = t.time_sk
    
    -- JOIN com dimensão QUALITY
    LEFT JOIN `project-id.dataset.dim_quality` q
        ON f.quality_sk = q.quality_sk

WHERE 
    -- Filtra agosto de 2020
    d.year = 2020
    AND d.month_number = 8
    AND f.record_status = 'active'

ORDER BY 
    f.updated_at DESC,
    f.fact_id;


-- Query 3: Versão analítica - Com agregações
SELECT 
    -- Agrupamento temporal
    d.full_date AS data_atualizacao,
    d.day_of_week_name AS dia_semana,
    
    -- Métricas agregadas
    COUNT(DISTINCT f.fact_id) AS total_fatos,
    COUNT(DISTINCT f.user_id) AS total_usuarios_distintos,
    
    -- Estatísticas de texto
    AVG(f.text_length) AS tamanho_medio_texto,
    MIN(f.text_length) AS tamanho_minimo_texto,
    MAX(f.text_length) AS tamanho_maximo_texto,
    
    -- Qualidade dos dados
    AVG(q.quality_score) AS score_qualidade_medio,
    AVG(q.data_completeness_pct) AS completude_media_pct,
    SUM(CASE WHEN q.has_validation_errors THEN 1 ELSE 0 END) AS total_com_erros,
    
    -- Status
    COUNT(CASE WHEN f.status = 'verified' THEN 1 END) AS total_verificados,
    COUNT(CASE WHEN f.status = 'pending' THEN 1 END) AS total_pendentes,
    
    -- Fontes
    STRING_AGG(DISTINCT s.api_source, ', ') AS fontes_api

FROM 
    `project-id.dataset.fact_cat_facts` f
    LEFT JOIN `project-id.dataset.dim_source` s ON f.source_sk = s.source_sk
    LEFT JOIN `project-id.dataset.dim_date` d ON DATE(f.updated_at) = d.full_date
    LEFT JOIN `project-id.dataset.dim_quality` q ON f.quality_sk = q.quality_sk

WHERE 
    d.year = 2020
    AND d.month_number = 8
    AND f.record_status = 'active'

GROUP BY 
    d.full_date,
    d.day_of_week_name,
    d.day_of_week

ORDER BY 
    d.full_date DESC;


-- Query 4: Versão para export - Formato simplificado para analytics
SELECT 
    f.fact_id,
    f.text AS cat_fact,
    f.text_length AS tamanho_texto,
    f.updated_at AS data_hora_atualizacao,
    DATE(f.updated_at) AS data_atualizacao,
    EXTRACT(HOUR FROM f.updated_at) AS hora_atualizacao,
    f.status,
    f.user_id,
    s.api_source AS fonte_dados,
    q.quality_score AS score_qualidade,
    CASE 
        WHEN q.has_validation_errors THEN 'Com erros'
        ELSE 'Sem erros'
    END AS status_validacao
    
FROM 
    `project-id.dataset.fact_cat_facts` f
    LEFT JOIN `project-id.dataset.dim_source` s ON f.source_sk = s.source_sk
    LEFT JOIN `project-id.dataset.dim_date` d ON DATE(f.updated_at) = d.full_date
    LEFT JOIN `project-id.dataset.dim_quality` q ON f.quality_sk = q.quality_sk

WHERE 
    d.year = 2020
    AND d.month_number = 8
    AND f.record_status = 'active'

ORDER BY 
    f.updated_at DESC;


/*
 * INSTRUÇÕES DE USO:
 * 
 * 1. Substitua 'project-id.dataset' pelo seu projeto e dataset real:
 *    Exemplo: `uol-catlovers.cat_facts_prod`
 * 
 * 2. Escolha a query apropriada:
 *    - Query 1: Dados brutos da tabela fato apenas
 *    - Query 2: Dados completos com todas as dimensões (recomendada)
 *    - Query 3: Análise agregada por dia
 *    - Query 4: Formato simplificado para export/analytics
 * 
 * 3. A query já filtra apenas registros ativos (record_status = 'active')
 * 
 * 4. Performance:
 *    - Use particionamento por updated_at na tabela fato
 *    - Considere clustering por source_sk e status
 *    - Dim_date é tabela conforma (pequena), sem impacto performance
 */
