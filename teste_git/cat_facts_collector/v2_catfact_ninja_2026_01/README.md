# 🐱 Cat Facts Extractor - V2 (catfact.ninja)

## 📌 Sobre

Versão configurada para usar a API alternativa catfact.ninja.

**API:** `https://catfact.ninja`  
**Status:** ✅ **ONLINE e FUNCIONAL**

---

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` baseado no `.env.example`:

```env
# API Configuration (catfact.ninja - ONLINE)
API_BASE_URL=https://catfact.ninja
API_TIMEOUT=30
API_MAX_RETRIES=3
API_RETRY_DELAY=2
API_VERIFY_SSL=True

# Output Configuration
OUTPUT_DIR=data
OUTPUT_FILENAME=cat_facts_ninja.csv

# Logging
LOG_LEVEL=INFO
```

---

## 🚀 Instalação

```bash
# Navegar até a pasta
cd cat_facts_collector/v2_catfact_ninja_2026_01

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

## ✅ Status Atual

Esta versão está **ATIVA** e funcional.

---

## 📊 Schema da API catfact.ninja

```json
{
  "current_page": 1,
  "data": [
    {
      "fact": "Cats have 32 muscles in each ear.",
      "length": 38
    }
  ],
  "first_page_url": "https://catfact.ninja/facts?page=1",
  "last_page": 34,
  "per_page": 10
}
```

**Características:**
- Retorna dados paginados
- Campos: `fact` e `length`
- Não tem upvotes, user, timestamps
- API simples e direta
