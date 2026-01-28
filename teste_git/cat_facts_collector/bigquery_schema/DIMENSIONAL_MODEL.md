# 🌟 Modelo Dimensional - Gold Layer (Para Analytics)

## 🎯 Visão Geral

Este é o **modelo dimensional Star Schema** da camada Gold, otimizado para o time de Analytics consumir dados de forma rápida e intuitiva.

```
            ┌─────────────┐
            │  dim_date   │
            │             │
            │ date_key PK │
            │ full_date   │
            │ day_name    │
            │ month_name  │
            │ quarter     │
            │ year        │
            └──────┬──────┘
                   │
                   │ date_key (FK)
                   │
    ┌──────────────┼──────────────┐
    │              │              │
┌───┴────┐  ┌─────▼─────────┐  ┌─┴────────┐
│dim_time│  │ FACT TABLE    │  │dim_source│
│        │  │ fact_cat_facts│  │          │
│time_key├──┤               ├──┤source_key│
│hour    │  │ fact_key PK   │  │source_   │
│minute  │  │ fact_text     │  │  name    │
│period  │  │ fact_length   │  │is_active │
└────────┘  │ upvotes_count │  └──────────┘
            │ quality_score │
            │               │
            │ source_key FK │
            │ date_key FK   │
            │ time_key FK   │
            │ quality_key FK│
            └───────┬───────┘
                    │
                    │ quality_key (FK)
                    │
              ┌─────▼────────┐
              │ dim_quality  │
              │              │
              │quality_key PK│
              │quality_tier  │
              │min_score     │
              │max_score     │
              └──────────────┘
```

---

## 📊 Tabela FATO: `fact_cat_facts`

### 🔑 Chaves

| Campo | Tipo | Descrição |
|-------|------|-----------|
| **fact_key** | INTEGER (PK) | Surrogate Key - Chave primária |
| **fact_id** | STRING | Business Key - ID de negócio |

### 📈 Métricas (Measures)

| Campo | Tipo | Descrição | Agregável? |
|-------|------|-----------|------------|
| **fact_text** | STRING | Texto do fact | ❌ Não |
| **fact_length** | INTEGER | Comprimento em caracteres | ✅ SIM (AVG, MIN, MAX, SUM) |
| **upvotes_count** | INTEGER | Número de upvotes | ✅ SIM (AVG, SUM, MAX) |
| **quality_score** | FLOAT64 | Score de qualidade (0-100) | ✅ SIM (AVG, MIN, MAX) |

### 🔗 Foreign Keys (Dimensões)

| Campo | Dimensão | Descrição |
|-------|----------|-----------|
| **source_key** | dim_source | Qual API originou |
| **date_key** | dim_date | Data da coleta |
| **time_key** | dim_time | Hora da coleta |
| **quality_key** | dim_quality | Tier de qualidade |

### 📝 Atributos Degenerados

| Campo | Tipo | Descrição |
|-------|------|-----------|
| **fact_type** | STRING | Categoria (cat, behavior, anatomy) |
| **is_verified** | BOOLEAN | Fact validado? |
| **ingestion_date** | DATE | Data de ingestão (particionamento) |

---

## 🗂️ Dimensões

### 1️⃣ `dim_source` - Fontes de Dados (SCD Tipo 1)

**Propósito:** Rastrear de qual API veio cada fact

| Campo | Tipo | Exemplo |
|-------|------|---------|
| **source_key** (PK) | INTEGER | `1` |
| **source_id** | STRING | `catfact-ninja` |
| **source_name** | STRING | `catfact.ninja` |
| **source_type** | STRING | `primary` |
| **is_active** | BOOLEAN | `true` |
| **api_endpoint** | STRING | `https://catfact.ninja/facts` |
| **effective_date** | DATE | `2024-01-01` |

**Dados exemplo:**
```sql
source_key | source_name                    | source_type  | is_active
-----------|--------------------------------|--------------|----------
1          | catfact.ninja                  | primary      | true
2          | catfacts-api.herokuapp.com     | alternative  | false
```

**Queries típicas:**
```sql
-- Facts por fonte ativa
SELECT s.source_name, COUNT(*) as total
FROM fact_cat_facts f
JOIN dim_source s ON f.source_key = s.source_key
WHERE s.is_active = true
GROUP BY s.source_name;
```

---

### 2️⃣ `dim_date` - Dimensão de Datas (SCD Tipo 0 - Conforma)

**Propósito:** Análises temporais (trends, sazonalidade, comparações)

| Campo | Tipo | Exemplo |
|-------|------|---------|
| **date_key** (PK) | INTEGER | `20260127` |
| **full_date** | DATE | `2026-01-27` |
| **day_of_week** | INTEGER | `2` (terça) |
| **day_name** | STRING | `Terça-feira` |
| **month** | INTEGER | `1` |
| **month_name** | STRING | `Janeiro` |
| **quarter** | INTEGER | `1` |
| **year** | INTEGER | `2026` |
| **is_weekend** | BOOLEAN | `false` |

**Queries típicas:**
```sql
-- Facts por dia da semana
SELECT d.day_name, COUNT(*) as total, AVG(f.fact_length) as avg_length
FROM fact_cat_facts f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.day_name
ORDER BY d.day_of_week;

-- Trend mensal
SELECT d.year, d.month_name, COUNT(*) as total_facts
FROM fact_cat_facts f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;
```

---

### 3️⃣ `dim_time` - Dimensão de Tempo (SCD Tipo 0 - Conforma)

**Propósito:** Análise intraday (horas de maior coleta, padrões horários)

| Campo | Tipo | Exemplo |
|-------|------|---------|
| **time_key** (PK) | INTEGER | `143045` |
| **hour** | INTEGER | `14` |
| **minute** | INTEGER | `30` |
| **second** | INTEGER | `45` |
| **period** | STRING | `Tarde` |

**Períodos do dia:**
- **Madrugada:** 00:00 - 05:59
- **Manhã:** 06:00 - 11:59
- **Tarde:** 12:00 - 17:59
- **Noite:** 18:00 - 23:59

**Queries típicas:**
```sql
-- Facts por período do dia
SELECT t.period, COUNT(*) as total, AVG(f.upvotes_count) as avg_upvotes
FROM fact_cat_facts f
JOIN dim_time t ON f.time_key = t.time_key
GROUP BY t.period
ORDER BY total DESC;

-- Horário de pico
SELECT t.hour, COUNT(*) as total
FROM fact_cat_facts f
JOIN dim_time t ON f.time_key = t.time_key
GROUP BY t.hour
ORDER BY total DESC
LIMIT 5;
```

---

### 4️⃣ `dim_quality` - Dimensão de Qualidade (SCD Tipo 1)

**Propósito:** Classificar e filtrar facts por qualidade

| Campo | Tipo | Exemplo |
|-------|------|---------|
| **quality_key** (PK) | INTEGER | `1` |
| **quality_tier** | STRING | `Excelente` |
| **min_score** | FLOAT64 | `90.0` |
| **max_score** | FLOAT64 | `100.0` |
| **tier_description** | STRING | `Facts de alta qualidade, verificados e únicos` |

**Tiers de Qualidade:**
```sql
quality_key | quality_tier | min_score | max_score | tier_description
------------|--------------|-----------|-----------|------------------
1           | Excelente    | 90.0      | 100.0     | Alta qualidade, verificados e únicos
2           | Bom          | 70.0      | 89.9      | Boa qualidade, pequenas inconsistências
3           | Razoável     | 50.0      | 69.9      | Qualidade aceitável, requer atenção
4           | Ruim         | 0.0       | 49.9      | Baixa qualidade, revisar ou descartar
```

**Queries típicas:**
```sql
-- Distribuição por qualidade
SELECT q.quality_tier, COUNT(*) as total, 
       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM fact_cat_facts f
JOIN dim_quality q ON f.quality_key = q.quality_key
GROUP BY q.quality_tier, q.min_score
ORDER BY q.min_score DESC;

-- Top facts de alta qualidade
SELECT f.fact_text, f.upvotes_count, q.quality_tier
FROM fact_cat_facts f
JOIN dim_quality q ON f.quality_key = q.quality_key
WHERE q.quality_tier = 'Excelente'
ORDER BY f.upvotes_count DESC
LIMIT 10;
```

---

## 🎯 Queries de Analytics (Exemplos Práticos)

### 📊 Dashboard Executivo

```sql
-- KPIs principais
SELECT 
  COUNT(DISTINCT fact_key) as total_facts,
  COUNT(DISTINCT date_key) as days_collected,
  ROUND(AVG(fact_length), 2) as avg_length,
  ROUND(AVG(quality_score), 2) as avg_quality,
  SUM(upvotes_count) as total_upvotes
FROM fact_cat_facts
WHERE ingestion_date >= CURRENT_DATE() - 30;
```

### 📈 Análise Temporal

```sql
-- Trend semanal com qualidade média
SELECT 
  d.year,
  d.month_name,
  EXTRACT(WEEK FROM d.full_date) as week,
  COUNT(*) as total_facts,
  ROUND(AVG(f.quality_score), 2) as avg_quality,
  ROUND(AVG(f.fact_length), 2) as avg_length
FROM fact_cat_facts f
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.full_date >= CURRENT_DATE() - 90
GROUP BY d.year, d.month_name, d.month, EXTRACT(WEEK FROM d.full_date)
ORDER BY d.year, d.month, week;
```

### 🏆 Top Performers

```sql
-- Top 10 facts mais populares de alta qualidade
SELECT 
  f.fact_text,
  f.fact_length,
  f.upvotes_count,
  s.source_name,
  d.full_date,
  q.quality_tier
FROM fact_cat_facts f
JOIN dim_source s ON f.source_key = s.source_key
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_quality q ON f.quality_key = q.quality_key
WHERE f.is_verified = true
  AND q.quality_tier = 'Excelente'
  AND f.upvotes_count IS NOT NULL
ORDER BY f.upvotes_count DESC
LIMIT 10;
```

### 🔍 Análise por Fonte

```sql
-- Comparação de métricas por fonte
SELECT 
  s.source_name,
  s.is_active,
  COUNT(*) as total_facts,
  ROUND(AVG(f.fact_length), 2) as avg_length,
  ROUND(AVG(f.quality_score), 2) as avg_quality,
  SUM(CASE WHEN f.is_verified THEN 1 ELSE 0 END) as verified_facts,
  ROUND(AVG(f.upvotes_count), 2) as avg_upvotes
FROM fact_cat_facts f
JOIN dim_source s ON f.source_key = s.source_key
GROUP BY s.source_name, s.is_active
ORDER BY total_facts DESC;
```

### 📅 Padrões Temporais

```sql
-- Fatos por dia da semana e período do dia
SELECT 
  d.day_name,
  t.period,
  COUNT(*) as total_facts,
  ROUND(AVG(f.quality_score), 2) as avg_quality
FROM fact_cat_facts f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_time t ON f.time_key = t.time_key
WHERE d.full_date >= CURRENT_DATE() - 30
GROUP BY d.day_of_week, d.day_name, t.period
ORDER BY d.day_of_week, 
  CASE t.period 
    WHEN 'Madrugada' THEN 1
    WHEN 'Manhã' THEN 2
    WHEN 'Tarde' THEN 3
    WHEN 'Noite' THEN 4
  END;
```

---

## 🏗️ DDL de Criação

### Tabela FATO

```sql
CREATE TABLE `cat_facts_dataset.fact_cat_facts`
(
  fact_key INT64 NOT NULL,
  fact_id STRING NOT NULL,
  fact_text STRING NOT NULL,
  fact_length INT64 NOT NULL,
  upvotes_count INT64,
  quality_score FLOAT64 NOT NULL,
  source_key INT64 NOT NULL,
  date_key INT64 NOT NULL,
  time_key INT64 NOT NULL,
  quality_key INT64 NOT NULL,
  fact_type STRING,
  is_verified BOOL NOT NULL,
  ingestion_date DATE NOT NULL
)
PARTITION BY ingestion_date
CLUSTER BY source_key, date_key, quality_key
OPTIONS(
  description="Tabela FATO do Gold Layer - Star Schema otimizado para Analytics",
  labels=[("layer", "gold"), ("table_type", "fact")]
);
```

### Dimensões

```sql
-- dim_source
CREATE TABLE `cat_facts_dataset.dim_source`
(
  source_key INT64 NOT NULL,
  source_id STRING NOT NULL,
  source_name STRING NOT NULL,
  source_type STRING NOT NULL,
  is_active BOOL NOT NULL,
  api_endpoint STRING NOT NULL,
  effective_date DATE NOT NULL
)
OPTIONS(
  description="Dimensão de fontes de dados (APIs) - SCD Tipo 1",
  labels=[("layer", "gold"), ("table_type", "dimension")]
);

-- dim_date
CREATE TABLE `cat_facts_dataset.dim_date`
(
  date_key INT64 NOT NULL,
  full_date DATE NOT NULL,
  day_of_week INT64 NOT NULL,
  day_name STRING NOT NULL,
  month INT64 NOT NULL,
  month_name STRING NOT NULL,
  quarter INT64 NOT NULL,
  year INT64 NOT NULL,
  is_weekend BOOL NOT NULL
)
OPTIONS(
  description="Dimensão de datas conforma - SCD Tipo 0",
  labels=[("layer", "gold"), ("table_type", "dimension")]
);

-- dim_time
CREATE TABLE `cat_facts_dataset.dim_time`
(
  time_key INT64 NOT NULL,
  hour INT64 NOT NULL,
  minute INT64 NOT NULL,
  second INT64 NOT NULL,
  period STRING NOT NULL
)
OPTIONS(
  description="Dimensão de tempo conforma - SCD Tipo 0",
  labels=[("layer", "gold"), ("table_type", "dimension")]
);

-- dim_quality
CREATE TABLE `cat_facts_dataset.dim_quality`
(
  quality_key INT64 NOT NULL,
  quality_tier STRING NOT NULL,
  min_score FLOAT64 NOT NULL,
  max_score FLOAT64 NOT NULL,
  tier_description STRING NOT NULL
)
OPTIONS(
  description="Dimensão de qualidade de dados - SCD Tipo 1",
  labels=[("layer", "gold"), ("table_type", "dimension")]
);
```

---

## 💡 Benefícios da Modelagem Dimensional

### ✅ Para o Time de Analytics

1. **Queries Intuitivas:**
   - JOINs simples e previsíveis
   - Dimensões descritivas (nomes, não IDs)
   - Estrutura Star Schema familiar

2. **Performance:**
   - Clustering otimizado para queries típicas
   - Particionamento por data
   - Pré-agregações através de dimensões

3. **Flexibilidade:**
   - Fácil adicionar novas dimensões
   - Drill-down/up natural (ano → mês → dia)
   - Slice and dice intuitivo

### ✅ Para o Negócio

1. **Análises Rápidas:**
   - Dashboards em tempo real
   - KPIs facilmente calculáveis
   - Trends e comparações simples

2. **Governança:**
   - Dimensões conforma (date, time)
   - SCDs documentados
   - Qualidade rastreável

3. **Escalabilidade:**
   - Fácil adicionar novos fatos
   - Dimensões compartilháveis
   - Modelo extensível

---

## 📚 Referências

- **Kimball Dimensional Modeling:** Star Schema, Conformed Dimensions, SCD Types
- **BigQuery Best Practices:** Partitioning, Clustering, Denormalization
- **Data Warehouse Toolkit:** Ralph Kimball & Margy Ross

---

## ✅ Conclusão

Este modelo dimensional:
- ✅ Star Schema clássico (1 fato + 4 dimensões)
- ✅ Otimizado para analytics (não para engenharia)
- ✅ Queries simples e intuitivas
- ✅ Performance otimizada (partitioning + clustering)
- ✅ Dimensões conforma (reutilizáveis)
- ✅ SCDs documentados (Tipo 0, Tipo 1)
- ✅ Pronto para ferramentas de BI (Looker, Tableau, etc.)
