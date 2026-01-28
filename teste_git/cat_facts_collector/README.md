

# 📁 Cat Facts Collector

Central dos pipelines, scripts e artefatos para coleta, processamento e disponibilização de fatos sobre gatos — núcleo do projeto de dados da UOLCatLovers.

**Data:** 27/01/2026  
**Autor:** UOLCatLovers Team

---

## 📑 Índice

- [Visão Geral](#visão-geral)
- [Estrutura de Pastas](#estrutura-de-pastas)
- [Comparativo Rápido: v1 vs v2](#comparativo-rápido-v1-vs-v2)
- [Como Usar](#como-usar)
- [Links Úteis](#links-úteis)
- [Status e Limitações](#status-e-limitações)
- [Troubleshooting](#troubleshooting)
- [Histórico de Desenvolvimento](#histórico-de-desenvolvimento)
- [Última Atualização](#última-atualização)

---

## 👀 Visão Geral

Esta pasta centraliza todos os pipelines, scripts e artefatos relacionados à coleta, processamento e disponibilização dos fatos sobre gatos.

---

## 📂 Estrutura de Pastas

```
cat_facts_collector/
├── README.md
├── v1_cat_fact_official_2026_01/   # Pipeline v1 (Heroku/offline)
├── v2_catfact_ninja_2026_01/       # Pipeline v2 (catfact.ninja/online)
├── bigquery_schema/                # Modelos, queries e documentação do BigQuery
└── ...
```

---

## ⚡ Comparativo Rápido: v1 vs v2

| Pipeline | Fonte/API                | Status         | Timestamps | Observações         |
|----------|-------------------------|---------------|------------|---------------------|
| v1       | cat-fact.herokuapp.com  | Offline (503) | Sim        | API oficial, Heroku |
| v2       | catfact.ninja           | Funcional     | Não        | Recomendada         |

---

## 🚀 Como Usar

### Opção 1: Scripts PowerShell (recomendado, na raiz do projeto)
- `../executar_v1_heroku.ps1` — Executa pipeline v1 (Heroku/offline)
- `../executar_v2_ninja.ps1` — Executa pipeline v2 (catfact.ninja/online)

### Opção 2: Execução Manual
- Instruções detalhadas em cada subpasta ([README v1](v1_cat_fact_official_2026_01/README.md), [README v2](v2_catfact_ninja_2026_01/README.md))

---

## 🔗 Links Úteis

- [BigQuery Schema](bigquery_schema/README.md)
- [Guia de Execução](GUIA_EXECUCAO.md)

---

## 🚦 Status e Limitações

- v1: API Heroku está offline (não testável)
- v2: Pipeline funcional, mas sem timestamps históricos

---

## 🛠️ Troubleshooting

- API Heroku offline? Use apenas o pipeline v2.
- Erro de dependência? Verifique ambiente virtual e requirements.txt.
- Permissão? Execute terminal como administrador.

---

## 📅 Histórico de Desenvolvimento

- 27/01/2026: Estrutura inicial, pipelines v1 e v2, documentação criada.

---

## 🕒 Última Atualização

28/01/2026

---
