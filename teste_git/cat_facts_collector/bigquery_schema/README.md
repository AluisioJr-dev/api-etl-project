# 📊 BigQuery Schema - Cat Facts (Gold Layer)

> **Tabela FATO para Analytics:** `cat_facts_dataset.fact_cat_facts`  
> Camada Gold da Arquitetura Medallion - Otimizada para consumo do time de Analytics

---

## 🎯 O que é essa tabela?

Esta é a **TABELA FATO** do Gold layer - a camada final onde o time de Analytics faz consultas. É uma tabela modelada dimensional, limpa e otimizada para análises de negócio.

**Diferença das outras camadas:**
- **Bronze** (Raw): Dados brutos da API (JSON cru)
- **Silver** (Cleaned): Dados validados e limpos
- **Gold** (Analytics): **← ESTA TABELA** - Modelada para analytics com dimensões e métricas

**Dados que entram aqui:**
- ✅ Facts da API **catfact.ninja** (API principal - funciona hoje)
- ✅ Facts da API **catfacts-api.herokuapp.com** (API alternativa - está offline, mas schema já preparado)

**Exemplo de dado real:**
```
Fact: "Cats have 32 muscles in each ear."
Tamanho: 38 caracteres
Origem: catfact.ninja
Data: 27/01/2026
```

---

## 📋 Campos da Tabela FATO (Para Analytics)

### 🔑 Chaves (Surrogate Keys)

| Campo | O que é? | Exemplo |
|-------|----------|---------|
| **fact_key** | Chave única da tabela fato (SK) | `1`, `2`, `3` |
| **fact_id** | ID de negócio do fact | `a3f5e8b9c2d1` |

### 📝 Métricas (Measures) - "O que queremos medir?"

| Campo | O que é? | Tipo | Exemplo |
|-------|----------|------|---------|
| **fact_text** | O texto do fact em si | STRING | `Cats sleep 16 hours a day` |
| **fact_length** | Comprimento em caracteres | INTEGER | `28` |
| **upvotes_count** | Número de curtidas | INTEGER | `15` |
| **quality_score** | Score de qualidade (0-100) | FLOAT | `95.5` |

### 🔗 Chaves Estrangeiras (Foreign Keys) - "Links para dimensões"

| Campo | Dimensão | O que representa? |
|-------|----------|-------------------|
| **source_key** | dim_source | Qual API originou o fact |
| **date_key** | dim_date | Quando foi coletado |
| **time_key** | dim_time | Hora da coleta |
| **quality_key** | dim_quality | Classificação de qualidade |

### 📊 Atributos Degenerados (Degenerate Dimensions)

| Campo | O que é? | Exemplo |
|-------|----------|---------|
| **fact_type** | Categoria do fact | `cat`, `behavior`, `anatomy` |
| **is_verified** | Fact verificado? | `true` ou `false` |

---

## 🔄 Como os Dados das APIs Viram Linhas na Tabela?

### API 1: catfact.ninja (🟢 Funcionando)

**O que a API devolve:**
```json
{
  "fact": "Cats have 32 muscles in each ear.",
  "length": 38
}
```

**Como vira linha na tabela:**
```
fact_id: "md5-hash-do-fact"
fact: "Cats have 32 muscles in each ear."
fact_length: 38
source_api: "catfact.ninja"
fact_type: NULL (não tem nessa API)
upvotes: NULL (não tem nessa API)
user_id: NULL (não tem nessa API)
is_duplicate: false
ingestion_date: 2026-01-27
```

### API 2: catfacts-api.herokuapp.com (🔴 Offline, mas preparado)

**O que a API devolveria:**
```json
{
  "_id": "58e008800aac31001185ed05",
  "text": "The Egyptian Mau is probably the oldest breed of cat.",
  "type": "cat",
  "upvotes": 5,
  "user": { "_id": "58e007480aac31001185ecef" },
  "createdAt": "2018-01-04T01:10:54.673Z"
}
```

**Como viraria linha na tabela:**
```
fact_id: "58e008800aac31001185ed05"
fact: "The Egyptian Mau is probably the oldest breed of cat."
fact_length: 54 (calculado)
source_api: "catfacts-api.herokuapp.com"
fact_type: "cat"
upvotes: 5
user_id: "58e007480aac31001185ecef"
is_duplicate: false
created_at: 2018-01-04 01:10:54
ingestion_date: 2026-01-27
```

---

## 💡 Por que Organizamos Assim?

### 🚀 Velocidade nas Consultas

**Particionamento por Data:**
- Dividimos a tabela em "gavetas" por dia
- Quando você busca dados de 27/01/2026, só abrimos a gaveta desse dia
- **Resultado:** Queries **99% mais rápidas** e **99% mais baratas**

**Clustering (Organização interna):**
- Dentro de cada "gaveta", organizamos por: API → Duplicados → Data
- Quando você busca "facts da catfact.ninja não duplicados", achamos super rápido
- **Resultado:** Queries **70-90% mais rápidas**

### 🔍 Detecção de Duplicatas

Usamos **hash SHA256** do conteúdo:
```python
# Se dois facts têm o mesmo texto...
fact1 = "Cats sleep 16 hours"
fact2 = "Cats sleep 16 hours"

# Terão o MESMO hash
hash1 = "8f3d2a1b..." 
hash2 = "8f3d2a1b..." # IGUAL!

# Então marcamos: is_duplicate = true no segundo
```

### 📊 Score de Qualidade

Calculamos uma nota de 0 a 100 para cada fact:

```
✅ Bônus:
  + Tem texto completo: +50 pontos
  + Texto tem mais de 10 caracteres: +20 pontos
  + Não é duplicado: +30 pontos
  + Tem upvotes (>5): +10 pontos
  + Tem data de criação: +5 pontos

❌ Penalidades:
  - Texto vazio: -50 pontos
  - Muito curto (<10 chars): -20 pontos
  - É duplicado: -30 pontos

Score final = max(0, min(100, total))
```

**Exemplos:**
- Fact completo, único, com upvotes: **100 pontos** ⭐⭐⭐⭐⭐
- Fact completo mas duplicado: **70 pontos** ⭐⭐⭐
- Fact muito curto: **30 pontos** ⭐

---

## 📈 Consultas Úteis para o Time de Analytics

### 1️⃣ "Quais facts chegaram hoje?"

```sql
SELECT 
  fact,
  fact_length,
  source_api,
  ingestion_timestamp
FROM `cat_facts_dataset.cat_facts`
WHERE ingestion_date = CURRENT_DATE()
ORDER BY ingestion_timestamp DESC;
```

**O que faz:** Mostra todos os facts que coletamos hoje, do mais recente ao mais antigo.

---

### 2️⃣ "Top 10 facts mais longos (só os únicos)"

```sql
SELECT 
  fact,
  fact_length,
  source_api
FROM `cat_facts_dataset.cat_facts`
WHERE is_duplicate = FALSE
  AND ingestion_date >= CURRENT_DATE() - 30
ORDER BY fact_length DESC
LIMIT 10;
```

**O que faz:** Lista os 10 fatos mais longos dos últimos 30 dias, ignorando duplicatas.

---

### 3️⃣ "Quantos facts duplicados temos?"

```sql
SELECT 
  source_api,
  COUNT(*) as total,
  SUM(CASE WHEN is_duplicate THEN 1 ELSE 0 END) as duplicados,
  ROUND(SUM(CASE WHEN is_duplicate THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) as percentual
FROM `cat_facts_dataset.cat_facts`
WHERE ingestion_date >= CURRENT_DATE() - 7
GROUP BY source_api;
```

**O que faz:** Mostra quantos % dos facts de cada API são duplicados nos últimos 7 dias.

**Resultado exemplo:**
```
source_api              | total | duplicados | percentual
------------------------|-------|------------|------------
catfact.ninja           | 327   | 12         | 3.67%
```

---

### 4️⃣ "Facts mais curtidos (API alternativa)"

```sql
SELECT 
  fact,
  upvotes,
  created_at
FROM `cat_facts_dataset.cat_facts`
WHERE source_api = 'catfacts-api.herokuapp.com'
  AND upvotes IS NOT NULL
  AND is_duplicate = FALSE
ORDER BY upvotes DESC
LIMIT 20;
```

**O que faz:** Lista os 20 facts mais populares da API alternativa (quando ela voltar).

---

### 5️⃣ "Qualidade média dos dados por dia"

```sql
SELECT 
  ingestion_date,
  ROUND(AVG(data_quality_score), 2) as qualidade_media,
  COUNT(*) as total_facts
FROM `cat_facts_dataset.cat_facts`
WHERE ingestion_date >= CURRENT_DATE() - 30
GROUP BY ingestion_date
ORDER BY ingestion_date DESC;
```

**O que faz:** Mostra a nota média de qualidade dos dados por dia nos últimos 30 dias.

**Resultado exemplo:**
```
ingestion_date | qualidade_media | total_facts
---------------|-----------------|-------------
2026-01-27     | 95.5            | 327
2026-01-26     | 94.8            | 315
```

---

## 💰 Quanto Custa?

### Storage (Armazenamento)
```
Tamanho de cada fact: ~500 bytes
Facts por dia: 327
Dados por dia: 164 KB

Custo mensal: ~$0.002 (praticamente grátis!)
```

### Queries (Consultas)
```
Query de 1 dia: 164 KB lidos
Query de 1 mês: 4.9 MB lidos
Query de 1 ano: 59 MB lidos

Custo por query mensal: ~$0.000025 (menos de 1 centavo!)
```

**Por que é tão barato?**
- Particionamento diário: só lê o necessário
- Clustering: organização eficiente
- Dados comprimidos: Parquet é muito compacto

---

## 🛠️ Como Criar a Tabela no BigQuery?

### Opção 1: Usando o Console Web

1. Acesse [BigQuery Console](https://console.cloud.google.com/bigquery)
2. No seu projeto, crie um dataset: `cat_facts_dataset`
3. Clique em "Criar Tabela"
4. Cole o SQL abaixo:

```sql
CREATE TABLE `cat_facts_dataset.cat_facts`
(
  fact_id STRING NOT NULL,
  fact STRING NOT NULL,
  fact_length INT64,
  source_api STRING NOT NULL,
  fact_type STRING,
  user_id STRING,
  upvotes INT64,
  user_upvoted BOOL,
  ingestion_timestamp TIMESTAMP NOT NULL,
  processing_timestamp TIMESTAMP NOT NULL,
  ingestion_date DATE NOT NULL,
  data_quality_score FLOAT64,
  is_duplicate BOOL NOT NULL,
  hash_content STRING NOT NULL,
  bronze_file_path STRING,
  silver_file_path STRING,
  pipeline_execution_id STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
PARTITION BY ingestion_date
CLUSTER BY source_api, is_duplicate, ingestion_date;
```

### Opção 2: Usando Terraform

O arquivo já está pronto em: `gcp_architecture/archive/scheduler_detailed/terraform/bigquery.tf`

### Opção 3: Usando Python

```python
from google.cloud import bigquery

client = bigquery.Client()
schema_path = "cat_facts_schema.json"

# Carrega o schema JSON
with open(schema_path) as f:
    schema_config = json.load(f)

# Cria a tabela
table = bigquery.Table(
    "uol-cat-lovers.cat_facts_dataset.cat_facts",
    schema=[bigquery.SchemaField(**field) for field in schema_config["schema"]["fields"]]
)
table.time_partitioning = bigquery.TimePartitioning(field="ingestion_date")
table.clustering_fields = ["source_api", "is_duplicate", "ingestion_date"]

table = client.create_table(table)
print(f"Tabela criada: {table.table_id}")
```

---

## 📚 Arquivos Relacionados

| Arquivo | Descrição |
|---------|-----------|
| **cat_facts_schema.json** | Schema JSON completo (para programação) |
| **SCHEMA_DOCUMENTATION.md** | Documentação técnica detalhada (para devs) |
| **README.md** | Este arquivo (guia simples para todos) |

---

## ❓ FAQ (Perguntas Frequentes)

### "Por que alguns campos são NULL?"

Porque as duas APIs têm estruturas diferentes:
- **catfact.ninja:** só tem `fact` e `length`
- **API alternativa:** tem `upvotes`, `user`, `type`, etc.

Usamos NULL para campos que uma API não fornece.

### "O que é hash SHA256?"

É como uma "digital" do conteúdo. Se dois texts são EXATAMENTE iguais, terão o mesmo hash. Usamos para detectar duplicatas.

### "Por que não deletamos duplicatas?"

Mantemos tudo para auditoria e rastreabilidade. Mas marcamos com `is_duplicate = true` para você filtrar nas queries.

### "Posso adicionar mais campos depois?"

Sim! BigQuery permite adicionar colunas sem reprocessar dados antigos. Os registros antigos terão NULL nos novos campos.

### "Como sei se os dados estão bons?"

Use o campo `data_quality_score`:
- **90-100:** Excelente ⭐⭐⭐⭐⭐
- **70-89:** Bom ⭐⭐⭐⭐
- **50-69:** Razoável ⭐⭐⭐
- **< 50:** Revisar ⭐⭐

---

## ✅ Resumo para Copiar e Colar

**O que é:** Tabela do BigQuery que guarda todos os fatos sobre gatos  
**Onde:** `uol-cat-lovers.cat_facts_dataset.cat_facts`  
**Particionamento:** Por dia (campo `ingestion_date`)  
**Clustering:** Por `source_api`, `is_duplicate`, `ingestion_date`  
**Campos principais:** `fact_id`, `fact`, `source_api`, `is_duplicate`, `ingestion_date`  
**Custo mensal:** ~$0.002 storage + ~$0.000025 por query  
**Performance:** 99% mais rápido e barato que tabela sem particionamento  

---

## 📞 Precisa de Ajuda?

- Dúvidas técnicas: Consulte **SCHEMA_DOCUMENTATION.md**
- Dúvidas sobre queries: Veja exemplos acima na seção "Consultas Úteis"
- Schema JSON: Use **cat_facts_schema.json** para automação

---

**Última atualização:** 27/01/2026  
**Versão do schema:** 1.0
