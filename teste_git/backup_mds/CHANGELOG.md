# Changelog

Todas as alterações importantes aplicadas ao repositório `teste_git`.

## 2026-01-27
- Restauradas pastas `v1_cat_fact_official_2026_01` e `v2_catfact_ninja_2026_01` após limpeza acidental.
- Corrigidos `src/config.py` em ambas as versões (endpoints e defaults separados para v1/v2).
- Adicionados `.env.example` em cada versão; remoção de `.env` do repositório.
- Criados scripts PowerShell portáteis: `executar_v1_heroku.ps1`, `executar_v2_ninja.ps1` (simplificados, sem blocos try/catch problemáticos).
- Ajustes de instalação pip: remoção de `--quiet` para visibilidade; uso de `--only-binary` quando apropriado; atualização de restrições de versão para compatibilidade com Python 3.13.
- Adicionadas dependências faltantes nos `requirements.txt`: `numpy`, `colorlog`, `urllib3`.
- Criados/atualizados scripts SQL em `cat_facts_collector/bigquery_schema/`:
  - `fact_extraction_august_2020.sql`
  - `qa_sample_extraction.sql` (inclui `EXPORT DATA` para GCS e SELECT para console)
  - `silver_fact_queries.sql`

## Notas
- Muitos ajustes foram feitos para facilitar execução local (PowerShell) e exportação de amostras para QA (BigQuery → GCS → CSV).
