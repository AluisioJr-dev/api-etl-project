# 🐱 Cat Facts Extractor - V1 (API Oficial - Heroku)

## 📌 Sobre

Versão configurada para usar a API oficial do Cat Facts hospedada no Heroku.

**API:** `https://cat-fact.herokuapp.com`  
**Status:** ⚠️ **OFFLINE** (API indisponível desde 2024)

---

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` baseado no `.env.example`:

```env
# API Configuration (Heroku - OFFLINE)
API_BASE_URL=https://cat-fact.herokuapp.com
API_TIMEOUT=30
API_MAX_RETRIES=3
API_RETRY_DELAY=2
API_VERIFY_SSL=False

# Output Configuration
OUTPUT_DIR=data
OUTPUT_FILENAME=cat_facts_heroku.csv

# Logging
LOG_LEVEL=INFO
```

---

## 🚀 Instalação

```bash
# Navegar até a pasta
cd cat_facts_collector/v1_cat_fact_official_2026_01

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

---

## ▶️ Execução

```bash
# Executar extração
python ./extract_cat_facts.py
```

---

## ⚠️ Status Atual

Esta versão está **desativada** porque a API Heroku está offline.

Use a **v2 (catfact.ninja)** que está funcional.

---

## 📊 Schema da API Heroku

```json
{
  "_id": "58e008800aac31001185ed05",
  "text": "The Egyptian Mau is probably the oldest breed of cat.",
  "type": "cat",
  "user": {
    "_id": "58e007480aac31001185ecef",
    "name": {
      "first": "Kasimir",
      "last": "Schulz"
    }
  },
  "upvotes": 5,
  "userUpvoted": false,
  "createdAt": "2018-01-04T01:10:54.673Z",
  "updatedAt": "2020-08-23T20:20:01.611Z"
}
```
