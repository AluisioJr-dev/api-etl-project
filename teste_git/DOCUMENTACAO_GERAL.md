# UOLCatLovers — Documentação Geral do Projeto

## 🐱 Visão Geral
A UOLCatLovers é uma startup de tecnologia pet que está desenvolvendo um aplicativo móvel para fornecer fatos curiosos e interessantes sobre gatos aos seus usuários. O objetivo é criar uma experiência divertida e educativa, utilizando dados reais extraídos da API pública Cat Facts ([documentação oficial](https://alexwohlbruck.github.io/cat-facts/docs/)).

## 🎯 Objetivo do Projeto
O projeto foi desenvolvido para atender à evolução natural de uma startup de dados, desde o MVP até uma solução escalável em nuvem:

1. **MVP Local:**
   - Desenvolver um script Python simples para extrair fatos sobre gatos da API Cat Facts e salvar em um arquivo CSV local.
   - Atende à demanda inicial, com baixo volume de dados e fácil execução.

2. **Escalabilidade e Nuvem:**
   - Com o crescimento do app e do volume de dados, projetar uma arquitetura na Google Cloud Platform (GCP) para extrair, armazenar e disponibilizar os dados de forma escalável e segura.
   - Permitir que os times de analytics e desenvolvimento acessem os dados facilmente.

3. **Empoderamento do Analytics:**
   - Especificar o esquema da tabela de fatos sobre gatos no BigQuery, detalhando campos, tipos e considerações para facilitar consultas e análises.

4. **Consultas SQL para Analytics e Dev:**
   - Criar consultas SQL para demandas reais dos times:
     - Extrair fatos atualizados em agosto de 2020 para estudos analíticos.
     - Gerar uma amostra aleatória de 10% dos registros para popular o ambiente de QA, exportando para CSV.

## 🚀 Resumo das Entregas
- Script Python funcional para extração e armazenamento local dos dados.
- Desenho de arquitetura escalável na GCP (sem necessidade de implementação).
- Especificação do schema BigQuery para dados de cat facts.
- Consultas SQL prontas para uso pelos times de analytics e desenvolvimento QA.

---

## 🔗 Links Úteis

- [Cat Facts API Documentation](https://alexwohlbruck.github.io/cat-facts/docs/)
- [Google Cloud BigQuery Documentation](https://cloud.google.com/bigquery/docs)
- [Google Cloud Functions Documentation](https://cloud.google.com/functions/docs)
- [Python Requests Library](https://requests.readthedocs.io/)

---

**Desenvolvido com ❤️ e 🐱 pela equipe UOLCatLovers**
