# 🚀 Scripts de Execução - Cat Facts Collector

## 📋 Visão Geral

Dois scripts PowerShell **prontos para distribuição** que configuram e executam automaticamente cada versão do projeto.

---

## 📦 Scripts Disponíveis

### 1️⃣ `executar_v1_heroku.ps1`
- **API:** cat-fact.herokuapp.com
- **Status:** ⚠️ OFFLINE
- **Output:** `cat_facts_heroku.csv`

### 2️⃣ `executar_v2_ninja.ps1`
- **API:** catfact.ninja
- **Status:** ✅ ONLINE
- **Output:** `cat_facts_ninja.csv`

---

## 🎯 Funcionalidades

### ✅ Setup Automático
- Verifica se Python está instalado
- Cria ambiente virtual automaticamente
- Instala todas as dependências
- Configura arquivo .env

### ✅ Execução Simplificada
- Ativa ambiente virtual automaticamente
- Executa extração de dados
- Exibe estatísticas ao final
- Retorna ao diretório original

### ✅ Portabilidade
- **Funciona em qualquer máquina Windows** com Python
- Detecta automaticamente o caminho do projeto
- Não requer configuração manual

---

## 🖥️ Como Usar

### Primeira Execução (Setup Completo)

```powershell
# V1 (Heroku - OFFLINE)
.\executar_v1_heroku.ps1 -Setup

# V2 (catfact.ninja - ONLINE) ⭐ RECOMENDADO
.\executar_v2_ninja.ps1 -Setup
```

### Execuções Seguintes

```powershell
# V1
.\executar_v1_heroku.ps1

# V2 ⭐ RECOMENDADO
.\executar_v2_ninja.ps1
```

### Reinstalação Limpa

```powershell
# Remove venv, data e logs antes de reinstalar
.\executar_v2_ninja.ps1 -CleanInstall
```

---

## 📊 O que o Script Faz

### 1. **Verificação de Ambiente**
```
✓ Python encontrado: Python 3.11.0
✓ Diretório de trabalho: C:\projeto\cat_facts_collector\v2_...
```

### 2. **Setup (Primeira Vez)**
```
✓ Ambiente virtual criado
✓ Ambiente virtual ativado
✓ Dependências instaladas
✓ Arquivo .env criado
```

### 3. **Execução**
```
═══════════════════════════════════════
  EXECUTANDO EXTRAÇÃO
═══════════════════════════════════════

[Logs da aplicação Python aqui...]
```

### 4. **Resultado**
```
✓ Extração concluída com sucesso!
  Tempo de execução: 00:05
  Arquivo: data\cat_facts_ninja.csv
  Linhas: 328
  Tamanho: 25.6 KB
```

---

## ⚙️ Parâmetros Disponíveis

| Parâmetro | Descrição |
|-----------|-----------|
| `-Setup` | Força setup completo (cria venv, instala deps) |
| `-CleanInstall` | Remove instalação anterior e reinstala tudo |
| *(sem parâmetros)* | Execução normal (usa venv existente) |

---

## 🔧 Requisitos

### Mínimos:
- **Windows** 10/11 ou Windows Server 2016+
- **PowerShell** 5.1+ (já vem com Windows)
- **Python** 3.8 ou superior

### Download Python:
👉 https://www.python.org/downloads/

---

## 📁 Estrutura Após Execução

```
teste_git/
├── executar_v1_heroku.ps1 ⭐ (este script)
├── executar_v2_ninja.ps1 ⭐ (este script)
└── cat_facts_collector/
    ├── v1_cat_fact_official_2026_01/
    │   ├── venv/ (criado automaticamente)
    │   ├── data/ (criado automaticamente)
    │   │   └── cat_facts_heroku.csv
    │   ├── logs/ (criado automaticamente)
    │   │   └── cat_facts_extraction.log
    │   └── .env (criado automaticamente)
    └── v2_catfact_ninja_2026_01/
        ├── venv/ (criado automaticamente)
        ├── data/ (criado automaticamente)
        │   └── cat_facts_ninja.csv ✅
        ├── logs/ (criado automaticamente)
        │   └── cat_facts_extraction.log
        └── .env (criado automaticamente)
```

---

## 🐛 Troubleshooting

### Erro: "não pode ser carregado porque a execução de scripts foi desabilitada"

**Solução:**
```powershell
# Abrir PowerShell como Administrador e executar:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Erro: "Python não encontrado"

**Solução:**
1. Instalar Python de https://www.python.org/downloads/
2. **Marcar opção**: "Add Python to PATH" durante instalação
3. Reiniciar terminal

### API V1 sempre falha

**Explicação:**
- API Heroku está OFFLINE desde 2024
- Isso é esperado - use a V2!

---

## 🎯 Recomendação

✅ **Use sempre `executar_v2_ninja.ps1`** - API funcional!

A V1 está mantida apenas para documentação.

---

## 📝 Exemplo de Execução Completa

```powershell
PS> .\executar_v2_ninja.ps1 -Setup

========================================
  Cat Facts Collector - V2 (ninja)
  API: catfact.ninja
  Status: ONLINE
========================================

Diretório de trabalho: C:\...\v2_catfact_ninja_2026_01

═══════════════════════════════════════
  SETUP INICIAL
═══════════════════════════════════════

Verificando instalação do Python...
✓ Python encontrado: Python 3.11.0

Criando ambiente virtual...
✓ Ambiente virtual criado

Ativando ambiente virtual...
✓ Ambiente virtual ativado

Instalando dependências...
✓ Dependências instaladas

Criando arquivo .env...
✓ Arquivo .env criado

═══════════════════════════════════════
  SETUP CONCLUÍDO!
═══════════════════════════════════════

═══════════════════════════════════════
  EXECUTANDO EXTRAÇÃO
═══════════════════════════════════════

API Online e funcional!

[Logs de execução...]

═══════════════════════════════════════
  RESULTADO
═══════════════════════════════════════

✓ Extração concluída com sucesso!
  Tempo de execução: 00:05
  Arquivo: data\cat_facts_ninja.csv
  Linhas: 328
  Tamanho: 25.6 KB

✓ Dados salvos com sucesso!
```

---

## 📞 Suporte

Para problemas, verifique:
1. **Logs:** `cat_facts_collector/v2_catfact_ninja_2026_01/logs/cat_facts_extraction.log`
2. **Arquivo .env** está configurado corretamente
3. **Python** está no PATH do sistema

---

**Última atualização:** 27/01/2026  
**Compatibilidade:** Windows 10/11, Python 3.8+
