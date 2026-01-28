# 🏗️ Arquiteturas GCP para Cat Facts Pipeline
**Questão 2 - UOLCatLovers | Análise Comparativa**

---

## 📋 Visão Geral

Este diretório contém **duas propostas de arquitetura** para implementar o pipeline de dados Cat Facts no Google Cloud Platform, usando a **Medallion Architecture** (Bronze → Silver → Gold).

### 🎯 Objetivo
Coletar dados da API de cat facts diariamente e disponibilizar no BigQuery para análises.

### 📊 Abordagens Disponíveis

| | 🔄 Serverless | 🏢 Enterprise |
|---|---|---|
| **Orquestração** | Cloud Scheduler | Cloud Composer (Airflow) |
| **Processamento** | Cloud Functions | Airflow + Dataflow |
| **Custo/mês** | ~$3-5 | ~$350-400 |
| **Complexidade** | ⭐ Baixa | ⭐⭐⭐⭐ Alta |
| **Use quando** | Pipeline simples | Pipeline complexo |

---

## 📁 Estrutura de Arquivos

```
gcp_architecture/
│
├── 📄 README.md (este arquivo)
│   └── Visão geral e links rápidos
│
├── 📊 comparison_diagram.md ⭐ COMECE AQUI
│   ├── Comparação visual side-by-side
│   ├── Matriz de decisão completa
│   ├── Quadrante de escolha
│   └── Recomendação para o projeto
│
├── 🔄 scheduler_approach/
│   └── architecture_diagram.md
│       ├── Mermaid detalhado (Serverless)
│       ├── Fluxo Bronze → Silver → Gold
│       ├── Vantagens e limitações
│       └── Custos: $3-5/mês
│
├── 🏢 airflow_approach/
│   └── architecture_diagram.md
│       ├── Mermaid detalhado (Enterprise)
│       ├── DAG com 7 tasks
│       ├── Orquestração completa
│       └── Custos: $350-400/mês
├── 📄 js
│   └── Mermaid JavaScript Lib
│   └── Utilizado em diagrams.html
│
└── 🌐 diagrams.html
    └── Comparação visual por html
    └── Visualização dos diagramas das soluções em arquitetura 
    └── Recomendações a partir dos cenários
```

---

## 🎨 Conceitos Principais

### 🥉🥈🥇 Medallion Architecture

```
Bronze Layer (Raw)
  ├─ Dados brutos da API
  ├─ Formato: JSON
  └─ Storage: GCS bucket

Silver Layer (Processed)
  ├─ Dados limpos e transformados
  ├─ Formato: Parquet
  └─ Storage: GCS bucket

Gold Layer (Analytics)
  ├─ Dados prontos para análise
  ├─ Agregações e métricas
  └─ Storage: BigQuery
```

### ⚡ Event-Driven vs Orchestrated

**Serverless (Event-Driven):**
```
Scheduler → Function 1 → GCS → Function 2 → GCS → Function 3 → BigQuery
            (HTTP)        (Event)           (Event)
```

**Airflow (Orchestrated):**
```
Composer → DAG
            ├─ Task 1 (extract)
            ├─ Task 2 (validate)
            ├─ Task 3 (transform)
            ├─ Task 4 (quality)
            ├─ Task 5 (load)
            ├─ Task 6 (aggregate)
            └─ Task 7 (notify)
```

---

## 💰 Análise de Custos

### Serverless - Breakdown Mensal
```
Cloud Scheduler:     $0.10  (30 jobs)
Cloud Functions:     $0.00  (free tier)
GCS Storage:         $0.02  (10 MB)
BigQuery Storage:    $0.01  (50 MB)
BigQuery Queries:    $0.50  (100 queries)
────────────────────────────
TOTAL:              ~$3-5
```

### Airflow - Breakdown Mensal
```
Cloud Composer:    $300.00  (environment medium)
GKE Cluster:        $30.00  (managed)
Dataflow:           $15.00  (30 jobs)
GCS Storage:         $0.10  (100 MB)
BigQuery:            $2.50  (storage + queries)
Cloud Logging:       $5.00  (10 GB)
────────────────────────────
TOTAL:           ~$350-400
```

**💡 Economia:** Serverless é **98% mais barato** para este projeto!

---

## ✅ Recomendação para Cat Facts

### 🏆 Escolha: **SERVERLESS**

**Por quê?**
- ✅ Volume de dados: 327 records/dia (~50 KB) - muito pequeno
- ✅ Custo: $3-5/mês vs $350-400/mês
- ✅ Simplicidade: Pipeline linear sem dependências complexas
- ✅ Manutenção: Praticamente zero
- ✅ Equipe: Projeto individual/pequena
- ✅ Frequência: 1x por dia

**Quando migrar para Airflow:**
- Volume > 10 GB/dia
- Múltiplas APIs/fontes
- SLA crítico (< 30 min)
- Equipe > 5 pessoas
- Orçamento > $500/mês

---

## 📊 Comparação Rápida

| Feature | Serverless | Airflow |
|---------|------------|---------|
| **Setup** | 10 min | 30 min |
| **Custo** | $5/mês | $400/mês |
| **UI Visual** | ❌ | ✅ |
| **Retry** | Básico | Avançado |
| **Timeout** | 9 min | Ilimitado |
| **Complexidade** | Baixa | Alta |
| **Best for** | < 10 GB/dia | > 10 GB/dia |

---

## 🔗 Links Importantes

### Documentação Oficial GCP
- [Cloud Functions](https://cloud.google.com/functions/docs)
- [Cloud Scheduler](https://cloud.google.com/scheduler/docs)
- [Cloud Composer](https://cloud.google.com/composer/docs)
- [BigQuery](https://cloud.google.com/bigquery/docs)
- [Cloud Storage](https://cloud.google.com/storage/docs)

### Tutoriais Relevantes
- [Event-driven Cloud Functions](https://cloud.google.com/functions/docs/calling/storage)
- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [Medallion Architecture](https://www.databricks.com/glossary/medallion-architecture)

---

**Data:** 27/01/2026  
**Autor:** GitHub Copilot  
**Projeto:** UOLCatLovers - Questão 2
