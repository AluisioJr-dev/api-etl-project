/*
 * EXTRAÇÃO DE AMOSTRA PARA AMBIENTE DE QA
 * 
 * Objetivo: Extrair 10% aleatório da base de cat facts
 * 
 * Campos retornados:
 * - text: Texto do fato sobre gatos
 * - created_at: Data de criação do registro
 * - updated_at: Data da última atualização
 * 
 * Output: CSV separado por vírgulas
 */

-- =============================================================
-- QUERY PRINCIPAL - Copie e execute no BigQuery Console
-- =============================================================

-- EXPORTA DIRETAMENTE PARA GCS (CSV)
-- Substitua 'gs://your-bucket/path/cat_facts_qa_*.csv' pelo seu bucket
EXPORT DATA
OPTIONS(
    uri='gs://your-bucket/path/cat_facts_qa_*.csv',
    format='CSV',
    header=true,
    field_delimiter=','
) AS
SELECT
    text,
    created_at,
    updated_at
FROM
    `project-id.dataset.fact_cat_facts`
WHERE
    record_status = 'active'
    AND RAND() < 0.1;  -- Aprox. 10%


-- =============================================================
-- QUERY SIMPLES (RETORNA DADOS) - Use para preview ou export manual
-- =============================================================
-- Esta query apenas retorna os dados (não escreve em GCS).
-- Útil para usar no BigQuery Console e clicar em "Save Results -> CSV (local file)"
SELECT
    text,
    created_at,
    updated_at
FROM
    `project-id.dataset.fact_cat_facts`
WHERE
    record_status = 'active'
    AND RAND() < 0.1
ORDER BY RAND();



-- =============================================================
-- COMO EXPORTAR PARA CSV
-- =============================================================

/*
 * PASSO 1: Execute a query acima no BigQuery Console
 * 
 * PASSO 2: Exporte os resultados
 *   - Clique no botão "SAVE RESULTS" 
 *   - Escolha "CSV (local file)"
 *   - Arquivo será baixado como "bq-results-XXXXXXXX.csv"
 * 
 * PASSO 3: Renomeie o arquivo
 *   - Sugestão: cat_facts_qa_sample.csv
 * 
 * PRONTO! O arquivo já está separado por vírgulas.
 */


-- =============================================================
-- VALIDAÇÃO (OPCIONAL)
-- =============================================================

-- Quantos registros existem na base completa?
SELECT 
    COUNT(*) AS total_registros
FROM 
    `project-id.dataset.fact_cat_facts`
WHERE 
    record_status = 'active';

-- A amostra deve ter aproximadamente 10% desse total.


-- =============================================================
-- NOTAS TÉCNICAS
-- =============================================================

/*
 * ANTES DE EXECUTAR:
 * - Substitua "project-id.dataset" pelo seu projeto real
 *   Exemplo: `uol-catlovers.cat_facts_prod`
 * 
 * CARACTERÍSTICAS DO CSV:
 * - Delimitador: vírgula (,)
 * - Encoding: UTF-8
 * - Headers: Sim (text, created_at, updated_at)
 * - Textos com vírgula: automaticamente entre aspas
 * 
 * SOBRE A AMOSTRA:
 * - Seleção aleatória, diferente a cada execução
 * - Aproximadamente 10% dos registros
 * - Apenas registros ativos (não deletados)
 */
