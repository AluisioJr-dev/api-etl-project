# 🏢 Arquitetura GCP - Cloud Composer + Airflow (Enterprise)
**Solução Robusta e Escalável | Medallion Architecture**

---

## 📊 Diagrama de Fluxo Detalhado

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'fontSize':'14px'}}}%%
graph TB
    %% ORCHESTRATION LAYER
    Composer[☁️ Cloud Composer 2.7<br/>━━━━━━━━━━━━━━━━━<br/>Managed Airflow<br/>Kubernetes Engine<br/>Auto-scaling workers]
    DAG[📜 DAG: cat_facts_medallion<br/>━━━━━━━━━━━━━━━━━<br/>Schedule: @daily<br/>Max Active Runs: 1<br/>Retries: 3]
    
    %% BRONZE LAYER
    subgraph Bronze["🥉 BRONZE LAYER - Extraction & Validation"]
        direction TB
        T1[Task 1: extract_api<br/>PythonOperator<br/>━━━━━━━━━━━<br/>GET catfact.ninja/facts<br/>Save raw JSON]
        T2[Task 2: validate_data<br/>PythonOperator<br/>━━━━━━━━━━━<br/>Schema validation<br/>Quality checks]
        GCS_B[(📦 GCS Bronze<br/><b>cat-facts-bronze</b><br/>━━━━━━━━━━━<br/>Format: JSON<br/>Version: enabled)]
    end
    
    %% SILVER LAYER
    subgraph Silver["🥈 SILVER LAYER - Transformation"]
        direction TB
        T3[Task 3: transform_dataflow<br/>DataflowPythonOperator<br/>━━━━━━━━━━━<br/>Apache Beam job<br/>Distributed processing]
        Beam{{⚡ Apache Beam<br/>Parallel workers<br/>Auto-scaling}}
        GCS_S[(📦 GCS Silver<br/><b>cat-facts-silver</b><br/>━━━━━━━━━━━<br/>Format: Parquet<br/>Partitioned by date)]
    end
    
    %% GOLD LAYER
    subgraph Gold["🥇 GOLD LAYER - Analytics"]
        direction TB
        T4[Task 4: quality_check<br/>PythonOperator<br/>━━━━━━━━━━━<br/>Data quality metrics<br/>Anomaly detection]
        T5[Task 5: load_bigquery<br/>BigQueryOperator<br/>━━━━━━━━━━━<br/>Load facts_raw<br/>Partitioned insert]
        T6[Task 6: aggregate_stats<br/>BigQueryOperator<br/>━━━━━━━━━━━<br/>Daily aggregations<br/>Summary tables]
        BQ[(🏢 BigQuery<br/><b>cat_facts_dataset</b><br/>━━━━━━━━━━━<br/>Tables: 3<br/>Partition: DAILY<br/>Cluster: fact)]
    end
    
    %% NOTIFICATION
    subgraph Notify["📢 Notifications"]
        T7[Task 7: send_notification<br/>SlackWebhookOperator<br/>━━━━━━━━━━━<br/>Success/Failure alerts<br/>Pipeline metrics]
        Slack{{💬 Slack Channel<br/>Real-time alerts}}
    end
    
    %% MONITORING
    subgraph Monitor["📈 Observability"]
        direction LR
        AirflowUI[🖥️ Airflow UI<br/>DAG visualization<br/>Task logs<br/>XCom browser]
        CloudMon[📊 Cloud Monitoring<br/>SLA tracking<br/>Resource metrics<br/>Custom dashboards]
        CloudLog[📝 Cloud Logging<br/>Centralized logs<br/>Error tracking<br/>Audit trail]
    end
    
    %% FLOW CONNECTIONS
    Composer --> DAG
    DAG --> T1
    T1 --> GCS_B
    GCS_B --> T2
    T2 -->|✅ Valid| T3
    T2 -->|❌ Invalid| T7
    
    T3 --> Beam
    Beam --> GCS_S
    GCS_S --> T4
    T4 -->|Quality OK| T5
    T4 -->|Quality Issues| T7
    
    T5 --> BQ
    T6 --> BQ
    T5 --> T6
    T6 --> T7
    T7 --> Slack
    
    Composer -.->|UI Access| AirflowUI
    DAG -.->|Metrics| CloudMon
    T1 -.->|Logs| CloudLog
    T3 -.->|Logs| CloudLog
    T5 -.->|Logs| CloudLog
    T6 -.->|Logs| CloudLog
    CloudLog -.->|Export| CloudMon
    
    %% STYLING
    classDef orchestration fill:#673ab7,stroke:#4527a0,stroke-width:3px,color:#fff
    classDef bronze fill:#34a853,stroke:#188038,stroke-width:3px,color:#fff
    classDef silver fill:#fbbc04,stroke:#f9ab00,stroke-width:3px,color:#000
    classDef gold fill:#ea4335,stroke:#c5221f,stroke-width:3px,color:#fff
    classDef storage fill:#e8f0fe,stroke:#4285f4,stroke-width:2px
    classDef notify fill:#ff6f00,stroke:#e65100,stroke-width:2px,color:#fff
    classDef monitor fill:#f1f3f4,stroke:#5f6368,stroke-width:2px
    
    class Composer,DAG orchestration
    class T1,T2,GCS_B bronze
    class T3,Beam,GCS_S silver
    class T4,T5,T6,BQ gold
    class T7,Slack notify
    class AirflowUI,CloudMon,CloudLog monitor
```

---

## 📋 Características da Solução

### ✅ Vantagens
| Aspecto | Benefício |
|---------|-----------|
| 🎨 **UI Visual** | Airflow UI completa para monitoramento |
| 🔄 **Orquestração** | Controle total de dependências e retries |
| 📊 **Observabilidade** | Logs, métricas e alertas integrados |
| 🔧 **Flexibilidade** | Suporta fluxos complexos e paralelos |
| 🚀 **Escalabilidade** | Auto-scaling de workers |
| 🛡️ **Confiabilidade** | SLA tracking, retry automático |
| 🔌 **Integrações** | 200+ providers prontos |

### ❌ Limitações
| Aspecto | Restrição |
|---------|-----------|
| 💰 **Custo** | $350-400/mês (alto para projetos pequenos) |
| 🏗️ **Complexidade** | Curva de aprendizado maior |
| ⏱️ **Setup** | Deployment leva ~30 minutos |
| 🔧 **Manutenção** | Requer conhecimento de Airflow |
| 📦 **Overhead** | Infraestrutura pesada para pipelines simples |

### 🎯 Casos de Uso Ideais
- ✅ Pipelines complexos com múltiplas dependências
- ✅ Alto volume de dados (> 10 GB/dia)
- ✅ Múltiplos pipelines coordenados
- ✅ Necessidade de SLA rigoroso
- ✅ Equipe grande com experiência em Airflow
- ✅ Ambiente enterprise com governança

---

## 💰 Estimativa de Custos (Mensal)

```
┌──────────────────────────┬────────────────┬────────────┐
│ Recurso                  │ Configuração   │ Custo      │
├──────────────────────────┼────────────────┼────────────┤
│ Cloud Composer (Medium)  │ 1 env          │ $300.00    │
│ ├─ Scheduler             │ 2 CPU, 7.5 GB  │            │
│ ├─ Web Server            │ 1 CPU, 3.75 GB │            │
│ └─ Workers (1-3)         │ 2 CPU, 7.5 GB  │            │
│ GKE (Composer backend)   │ Auto-managed   │ $30.00     │
│ Cloud Storage            │ 100 MB         │ $0.10      │
│ BigQuery Storage         │ 200 MB         │ $0.05      │
│ BigQuery Queries         │ 500 queries    │ $2.50      │
│ Dataflow Jobs            │ 30 jobs/mês    │ $15.00     │
│ Cloud Logging            │ 10 GB/mês      │ $5.00      │
├──────────────────────────┴────────────────┼────────────┤
│ TOTAL MENSAL                              │ ~$350-400  │
└───────────────────────────────────────────┴────────────┘
```

**Otimizações possíveis:**
- 🔻 Environment Small: -$100/mês
- 🔻 Schedule Off-hours: -$50/mês (parar env quando não usar)
- 🔻 Development env: ~$200/mês (config reduzida)

---

## 🏗️ Recursos Criados

**GCP Services:**
- 1× Cloud Composer 2.7 environment
- 1× GKE cluster (managed)
- 2× GCS Buckets (Bronze, Silver) + DAGs bucket
- 1× BigQuery Dataset + 3 Tables
- 2× Service Accounts (Composer, Dataflow)
- VPC + Subnetwork
- Cloud Logging + Monitoring + Alerting

**Airflow Components:**
- 1× DAG com 7 tasks
- 5× Operators (Python, Dataflow, BigQuery, Slack)
- Task Groups para organização
- XCom para comunicação entre tasks
- SLA tracking e alertas

**Detalhes técnicos arquivados em:** `../archive/airflow_detailed/`
