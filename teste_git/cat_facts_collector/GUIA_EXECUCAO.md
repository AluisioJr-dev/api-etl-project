# 🚀 Guia de Execução das Soluções

## 📌 Resumo

Cada solução está **isolada** em sua própria pasta com:
- ✅ Ambiente virtual próprio
- ✅ Dependências próprias
- ✅ Variáveis de ambiente específicas
- ✅ Dados e logs separados

**Não há conflito** entre as soluções - você pode executar ambas simultaneamente!

---

## 🔧 Solução 1: cat-fact.herokuapp.com (OFFLINE)

### Pasta
```
cat_facts_collector/v1_cat_fact_official_2026_01/
```

### Setup

```bash
# 1. Navegar até a pasta
cd cat_facts_collector/v1_cat_fact_official_2026_01

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar ambiente virtual (Windows)
venv\Scripts\activate

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Configurar .env
copy .env.example .env
# Editar .env com suas configurações
```

### Executar

```bash
python src/extract_cat_facts.py
```

### ⚠️ Status
**API OFFLINE** - Esta solução não funciona no momento.

---

## 🔧 Solução 2: catfact.ninja (FUNCIONAL)

### Pasta
```
cat_facts_collector/v2_catfact_ninja_2026_01/
```

### Setup

```bash
# 1. Navegar até a pasta
cd cat_facts_collector/v2_catfact_ninja_2026_01

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar ambiente virtual (Windows)
venv\Scripts\activate

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Configurar .env
copy .env.example .env
# Editar .env com suas configurações
```

### Executar

```bash
python src/extract_cat_facts.py
```

### ✅ Status
**API ONLINE** - Esta solução está funcional!

---

## 🎯 Scripts PowerShell para Execução Rápida

### executar_solucao1.ps1 (Heroku)

```powershell
cd cat_facts_collector/v1_cat_fact_official_2026_01
venv\Scripts\activate
python src/extract_cat_facts.py
```

### executar_solucao2.ps1 (ninja)

```powershell
cd cat_facts_collector/v2_catfact_ninja_2026_01
venv\Scripts\activate
python src/extract_cat_facts.py
```

---

## 📊 Estrutura de Dados

### Outputs

Cada solução salva seus dados em:
- **Solução 1:** `v1_cat_fact_official_2026_01/data/cat_facts_heroku.csv`
- **Solução 2:** `v2_catfact_ninja_2026_01/data/cat_facts_ninja.csv`

### Logs

Cada solução gera logs em:
- **Solução 1:** `v1_cat_fact_official_2026_01/logs/cat_facts_extraction.log`
- **Solução 2:** `v2_catfact_ninja_2026_01/logs/cat_facts_extraction.log`

---

## 🔄 Comparação das Saídas

### API Heroku (Solução 1)

```csv
_id,text,type,upvotes,createdAt,updatedAt,...
58e00880...,The Egyptian Mau...,cat,5,2018-01-04,...
```

**Campos:** `_id`, `text`, `type`, `user`, `upvotes`, `createdAt`, `updatedAt`

### API ninja (Solução 2)

```csv
fact,length,extracted_at
Cats have 32 muscles...,38,2026-01-27 14:30:00
```

**Campos:** `fact`, `length`, `extracted_at`

---

## ✅ Recomendação

**Use a Solução 2 (catfact.ninja)** pois está funcional.

A Solução 1 está mantida apenas para documentação e caso a API Heroku volte ao ar.
