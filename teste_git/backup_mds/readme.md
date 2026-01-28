# UOLCatLovers - Cat Facts Data Engineering Project

## 📋 Sobre o Projeto

A **UOLCatLovers** é uma startup de tecnologia pet que desenvolve um aplicativo móvel fornecendo fatos interessantes sobre gatos para seus usuários. Este repositório contém as soluções de engenharia de dados para extração, armazenamento e disponibilização dos dados de fatos sobre gatos.

Os dados são extraídos da **Cat Facts API**.  
📖 Documentação: https://alexwohlbruck.github.io/cat-facts/docs/

---

## 🎯 Objetivos do Projeto

Este projeto foi desenvolvido para atender às seguintes necessidades:

1. **Extração inicial de dados**: Script Python para extrair dados da API e salvar localmente em CSV
2. **Arquitetura em nuvem**: Solução escalável na Google Cloud Platform (GCP)
3. **Esquema de dados**: Definição de tabela BigQuery para análise
4. **Consultas SQL**: Queries para atender demandas dos times de Analytics e Desenvolvimento

---


## 📂 Estrutura do Repositório

```
teste_git/
├── readme.md                  # Este arquivo
├── CHANGELOG.md               # Histórico de alterações
├── executar_v1_heroku.ps1     # Script PowerShell: executa pipeline v1 (Heroku/offline)
├── executar_v2_ninja.ps1      # Script PowerShell: executa pipeline v2 (catfact.ninja/online)
├── cat_facts_collector/       # Pipelines e documentação principal
│   ├── README.md                  # Documentação geral dos pipelines
│   ├── v1_cat_fact_official_2026_01/   # Pipeline v1 (API Heroku, atualmente offline)
│   ├── v2_catfact_ninja_2026_01/       # Pipeline v2 (API catfact.ninja, funcional)
│   └── bigquery_schema/                # Modelos, queries e documentação do BigQuery
└── ...
```
---

## 🚀 Soluções Desenvolvidas

### 1. Script Python para Extração de Dados (Solução Local)

**Objetivo**: Desenvolver um script Python que extraia dados da Cat Facts API e salve em arquivo CSV local.

**Localização**: `src/extract_cat_facts.py`

**Funcionalidades**:
- Consumo da API Cat Facts
- Tratamento de erros e retry logic
- Salvamento em formato CSV
- Logging de execução

**Como executar**:
```bash
pip install -r requirements.txt
python src/extract_cat_facts.py
```

---

### 2. Arquitetura na Google Cloud Platform

**Objetivo**: Projetar arquitetura escalável para extrair, armazenar e disponibilizar dados na nuvem.

**Localização**: `architecture/gcp_architecture.md`

Este projeto apresenta **duas abordagens de orquestração** para atender diferentes necessidades:

---

#### 🔹 **Arquitetura 1: Solução Serverless com Cloud Scheduler**

**Ideal para**: Pipelines simples, baixo volume de dados, execuções agendadas regulares

**Componentes**:
- **Cloud Scheduler**: Agendamento de execuções periódicas (cron jobs)
- **Cloud Functions**: Função serverless para extração da API
- **Cloud Storage**: Armazenamento de dados brutos (Data Lake - camada Bronze)
- **Cloud Dataflow**: Processamento e transformação de dados (ETL)
- **BigQuery**: Data Warehouse para consultas analíticas
- **Cloud Logging/Monitoring**: Observabilidade, logs e alertas
- **Pub/Sub** (opcional): Mensageria para comunicação assíncrona entre componentes

**Fluxo de dados**:
```
┌─────────────────┐
│ Cloud Scheduler │ (Trigger diário: 0 2 * * *)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Cloud Function  │ (Extração da API Cat Facts)
│  extract_facts  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Cloud Storage   │ (gs://bucket-name/raw/cat_facts_{date}.json)
│   (Raw/Bronze)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Cloud Dataflow │ (Transformação e Validação)
│   (ETL Pipeline)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    BigQuery     │ (dataset.cat_facts - Particionada)
│  (Gold Layer)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Analytics Teams │ (Looker Studio, Data Studio, etc.)
└─────────────────┘
```

**Vantagens**:
- ✅ Baixo custo operacional (pay-per-use)
- ✅ Zero gerenciamento de infraestrutura
- ✅ Escalabilidade automática
- ✅ Implementação rápida e simples
- ✅ Ideal para pipelines lineares

**Desvantagens**:
- ❌ Orquestração limitada para pipelines complexos
- ❌ Difícil gerenciar dependências entre múltiplas tarefas
- ❌ Menor visibilidade do pipeline completo
- ❌ Retry logic precisa ser implementado manualmente

---

#### 🔹 **Arquitetura 2: Solução Robusta com Cloud Composer (Apache Airflow)**

**Ideal para**: Pipelines complexos, múltiplas dependências, alto volume, governança de dados

**Componentes**:
- **Cloud Composer (Airflow)**: Orquestração completa de workflows
- **Cloud Functions/Cloud Run**: Execução de tarefas específicas
- **Cloud Storage**: Data Lake (camadas Bronze, Silver, Gold)
- **BigQuery**: Data Warehouse e processamento analítico
- **Cloud Dataproc** (opcional): Processamento Spark para grandes volumes
- **Cloud Logging/Monitoring**: Observabilidade e alertas
- **Secret Manager**: Gerenciamento seguro de credenciais

**Fluxo de dados (DAG Airflow)**:
```
┌──────────────────────────────────────────────────────────────────┐
│                     Cloud Composer (Airflow)                      │
│                                                                    │
│  DAG: cat_facts_daily_pipeline                                   │
│                                                                    │
│  ┌──────────────┐                                                │
│  │ check_api    │ (Verifica disponibilidade da API)              │
│  │ availability │                                                │
│  └──────┬───────┘                                                │
│         │                                                         │
│         ▼                                                         │
│  ┌──────────────┐                                                │
│  │extract_facts │ (Cloud Function/Operator)                      │
│  │   from_api   │ → Cloud Storage (Bronze)                       │
│  └──────┬───────┘                                                │
│         │                                                         │
│         ▼                                                         │
│  ┌──────────────┐                                                │
│  │validate_data │ (Great Expectations/Python)                    │
│  │              │                                                │
│  └──────┬───────┘                                                │
│         │                                                         │
│         ▼                                                         │
│  ┌──────────────┐                                                │
│  │ transform_   │ (Dataproc/Dataflow/BigQuery)                   │
│  │   and_clean  │ → Cloud Storage (Silver)                       │
│  └──────┬───────┘                                                │
│         │                                                         │
│         ▼                                                         │
│  ┌──────────────┐                                                │
│  │  load_to_bq  │ (BigQueryInsertJobOperator)                    │
│  │              │ → BigQuery (Gold - Particionado)               │
│  └──────┬───────┘                                                │
│         │                                                         │
│         ▼                                                         │
│  ┌──────────────┐                                                │
│  │ data_quality │ (Testes de qualidade de dados)                 │
│  │   checks     │                                                │
│  └──────┬───────┘                                                │
│         │                                                         │
│         ▼                                                         │
│  ┌──────────────┐                                                │
│  │  send_slack  │ (Notificação de sucesso/falha)                 │
│  │notification  │                                                │
│  └──────────────┘                                                │
│                                                                    │
└──────────────────────────────────────────────────────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │    BigQuery      │
                  │  (dataset.       │
                  │   cat_facts)     │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Analytics Teams  │
                  │ & Applications   │
                  └──────────────────┘
```

**Estrutura de Camadas (Medallion Architecture)**:
```
Cloud Storage:
├── bronze/          # Dados brutos da API (JSON)
│   └── cat_facts/
│       └── year=2026/
│           └── month=01/
│               └── day=26/
│                   └── cat_facts_20260126_*.json
│
├── silver/          # Dados limpos e validados (Parquet)
│   └── cat_facts/
│       └── year=2026/
│           └── cat_facts_*.parquet
│
└── gold/            # Dados agregados/otimizados (backup)
    └── cat_facts/
        └── cat_facts_analytics_*.parquet

BigQuery:
└── dataset_prod/
    ├── cat_facts (tabela principal - particionada)
    ├── cat_facts_staging
    └── cat_facts_quality_metrics
```

**DAG Airflow - Principais Operators**:
```python
from airflow import DAG
from airflow.providers.google.cloud.operators.functions import CloudFunctionInvokeFunctionOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'email': ['data-team@uolcatlovers.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'cat_facts_daily_pipeline',
    default_args=default_args,
    description='Pipeline diário de Cat Facts',
    schedule_interval='0 2 * * *',  # 2 AM diariamente
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['cat-facts', 'daily', 'api'],
) as dag:
    
    # Tasks definidas no diagrama acima
    ...
```

**Vantagens**:
- ✅ Orquestração visual e completa de workflows
- ✅ Gerenciamento robusto de dependências e paralelismo
- ✅ Retry automático e tratamento de falhas
- ✅ Monitoramento detalhado de cada etapa
- ✅ Versionamento de DAGs
- ✅ Backfill e reprocessamento facilitado
- ✅ Integração nativa com todo ecossistema GCP
- ✅ SLAs e alertas configuráveis

**Desvantagens**:
- ❌ Custo mais elevado (ambiente Composer sempre ativo)
- ❌ Curva de aprendizado do Airflow
- ❌ Maior complexidade inicial de setup
- ❌ Overhead para pipelines muito simples

---

#### 📊 **Comparação entre as Arquiteturas**

| Critério | Cloud Scheduler | Cloud Composer (Airflow) |
|----------|-----------------|--------------------------|
| **Complexidade** | Baixa | Média-Alta |
| **Custo** | Muito baixo | Médio-Alto |
| **Escalabilidade** | Alta (serverless) | Muito Alta |
| **Orquestração** | Limitada | Completa |
| **Visibilidade** | Básica (logs) | Avançada (UI Airflow) |
| **Manutenção** | Mínima | Moderada |
| **Retry Logic** | Manual | Automático |
| **Dependências** | Difícil | Nativo |
| **Ideal para** | MVPs, pipelines simples | Produção enterprise |
| **Time to Market** | Rápido (dias) | Médio (semanas) |

---

#### 🎯 **Recomendação**

**Para a UOLCatLovers**:

- **Fase Inicial (MVP)**: Usar **Arquitetura 1 (Cloud Scheduler)** 
  - Baixo custo e rápida implementação
  - Suficiente para validar o produto

- **Crescimento**: Migrar para **Arquitetura 2 (Airflow)** quando:
  - Volume de dados > 1GB/dia
  - Necessidade de múltiplas fontes de dados
  - Pipelines com mais de 3 etapas interdependentes
  - Time de dados com 2+ engenheiros
  - Necessidade de governança e compliance

---

### 3. Esquema da Tabela BigQuery

**Objetivo**: Especificar o esquema da tabela de cat facts no BigQuery.

**Localização**: `schema/cat_facts_bigquery_schema.json`

**Campos da tabela `cat_facts`**:

| Campo | Tipo | Modo | Descrição |
|-------|------|------|-----------|
| id | STRING | REQUIRED | Identificador único do fato |
| text | STRING | REQUIRED | Texto do fato sobre gatos |
| type | STRING | NULLABLE | Tipo/categoria do fato |
| user_id | STRING | NULLABLE | ID do usuário que criou o fato |
| upvotes | INTEGER | NULLABLE | Número de votos positivos |
| created_at | TIMESTAMP | REQUIRED | Data/hora de criação |
| updated_at | TIMESTAMP | REQUIRED | Data/hora da última atualização |
| deleted | BOOLEAN | NULLABLE | Indicador se o fato foi deletado |
| source | STRING | NULLABLE | Origem do fato |
| used | BOOLEAN | NULLABLE | Indicador se o fato foi usado |
| ingestion_date | DATE | REQUIRED | Data de ingestão no BigQuery |
| ingestion_timestamp | TIMESTAMP | REQUIRED | Timestamp de ingestão no BigQuery |

**Considerações**:
- Particionamento por `ingestion_date` para otimização de consultas e custo
- Clustering por `updated_at` para queries temporais
- Campos de auditoria (`ingestion_date`, `ingestion_timestamp`) para rastreabilidade

---

### 4. Consulta SQL - Fatos Atualizados em Agosto/2020

**Objetivo**: Extrair fatos atualizados em agosto de 2020 para estudo de caso do time de Analytics.

**Localização**: `src/queries/august_2020_facts.sql`

**Query**:
```sql
SELECT 
    id,
    text,
    type,
    user_id,
    upvotes,
    created_at,
    updated_at,
    deleted,
    source,
    used
FROM 
    `project-id.dataset.cat_facts`
WHERE 
    DATE(updated_at) BETWEEN '2020-08-01' AND '2020-08-31'
    AND deleted IS NOT TRUE
ORDER BY 
    updated_at DESC;
```

---

### 5. Consulta SQL - Amostra Aleatória 10% para QA

**Objetivo**: Extrair 10% aleatório dos registros para ambiente de QA, exportando para CSV.

**Localização**: `src/queries/random_sample_10pct.sql`

**Query**:
```sql
SELECT 
    text,
    created_at,
    updated_at
FROM 
    `project-id.dataset.cat_facts`
WHERE 
    RAND() < 0.1
ORDER BY 
    RAND();
```

**Exportação para CSV**:
```bash
bq extract \
  --destination_format CSV \
  --field_delimiter ',' \
  --print_header=true \
  'project-id:dataset.cat_facts_sample' \
  gs://bucket-name/cat_facts_qa_sample.csv
```

**Alternativa usando CLI do BigQuery**:
```bash
bq query \
  --use_legacy_sql=false \
  --format=csv \
  --max_rows=1000000 \
  'SELECT text, created_at, updated_at 
   FROM `project-id.dataset.cat_facts` 
   WHERE RAND() < 0.1 
   ORDER BY RAND()' > cat_facts_qa_sample.csv
```

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal para scripts
- **Google Cloud Platform**: Infraestrutura em nuvem
  - BigQuery
  - Cloud Functions
  - Cloud Storage
  - Cloud Scheduler
  - Dataflow
- **SQL**: Consultas analíticas
- **Libraries Python**:
  - `requests`: Consumo da API
  - `pandas`: Manipulação de dados
  - `google-cloud-bigquery`: Integração com BigQuery
  - `google-cloud-storage`: Integração com Cloud Storage

---

## 📊 Dados da API Cat Facts

A API fornece os seguintes endpoints principais:

- `GET /facts`: Lista todos os fatos sobre gatos
- `GET /facts/random`: Retorna um fato aleatório
- `GET /facts/{id}`: Retorna um fato específico

**Exemplo de resposta**:
```json
{
  "_id": "591f9894d369931519ce358f",
  "text": "A cat's hearing is better than a dog's.",
  "type": "cat",
  "user": {
    "_id": "587288bb2f814b9c57a9040f",
    "name": {
      "first": "Alex",
      "last": "Wohlbruck"
    }
  },
  "upvotes": 4,
  "userUpvoted": null,
  "createdAt": "2018-01-04T01:10:54.673Z",
  "updatedAt": "2020-08-23T20:20:01.611Z"
}
```

---

## 📝 Requisitos

### Para execução local (Questão 1):
```bash
pip install requests pandas python-dotenv
```

### Para integração com GCP:
```bash
pip install google-cloud-bigquery google-cloud-storage
```

**Arquivo `requirements.txt`**:
```
requests>=2.28.0
pandas>=1.5.0
google-cloud-bigquery>=3.0.0
google-cloud-storage>=2.0.0
python-dotenv>=0.20.0
```

---

## 🔒 Boas Práticas Implementadas

1. **Segurança**:
   - Credenciais armazenadas em variáveis de ambiente
   - Service accounts com permissões mínimas necessárias
   
2. **Qualidade de Dados**:
   - Validação de dados antes da ingestão
   - Deduplicação baseada em ID
   - Tratamento de valores nulos
   
3. **Performance**:
   - Particionamento de tabelas BigQuery
   - Clustering para otimização de queries
   - Batch processing para volumes grandes
   
4. **Monitoramento**:
   - Logging estruturado
   - Alertas para falhas de pipeline
   - Métricas de SLA

5. **Documentação**:
   - README detalhado
   - Comentários no código
   - Esquemas versionados

---

## 📈 Evolução da Solução

### Fase 1: Solução Local (MVP)
- Script Python simples
- Armazenamento em CSV local
- Execução manual

### Fase 2: Solução em Nuvem (Escalável)
- Arquitetura serverless na GCP
- Processamento automatizado
- Armazenamento escalável
- Acesso via BigQuery

### Fase 3: Próximos Passos
- [ ] Implementar CI/CD com Cloud Build
- [ ] Adicionar testes automatizados
- [ ] Criar dashboards no Power BI ou Looker
- [ ] Implementar Data Quality checks com Great Expectations
- [ ] Adicionar streaming com Pub/Sub para dados em tempo real

---

## 👥 Time

**Engenharia de Dados - UOLCatLovers**

---

## 📄 Licença

Este projeto foi desenvolvido como parte de um case técnico para avaliação.

---

## 🔗 Links Úteis

- [Cat Facts API Documentation](https://alexwohlbruck.github.io/cat-facts/docs/)
- [Google Cloud BigQuery Documentation](https://cloud.google.com/bigquery/docs)
- [Google Cloud Functions Documentation](https://cloud.google.com/functions/docs)
- [Python Requests Library](https://requests.readthedocs.io/)

---

**Desenvolvido com ❤️ e 🐱 pela equipe UOLCatLovers**
