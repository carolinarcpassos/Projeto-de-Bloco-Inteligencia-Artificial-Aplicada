# Project Charter - IncluaTech (Inclusão PcD no Mercado de Trabalho)

## 1. Visão Geral
* **Nome do Projeto:** IncluaTech
* **Pergunta Afiada (Sharp Question):** Quais estados brasileiros e setores econômicos apresentam os maiores déficits de contratação de pessoas com deficiência em relação ao que é exigido pela Lei de Cotas (Lei nº 8.213/1991)?
* **Público-Alvo:** Equipes de RH, Lideranças de ESG e Profissionais PcD.
* **Cientista de Dados:** Carolina Ramos da Costa Passos.

## 2. Metas e Indicadores de Sucesso (SMART)
* **Entrega técnica:** Desenvolver um dashboard interativo no Streamlit contendo a análise de conformidade de contratação de PcDs por UF e setor econômico, permitindo a comparação de cenários em poucos cliques.
* **Impacto de negócio:** Permitir que gestores de Atração de Talentos e analistas ESG identifiquem os gargalos de contratação mais críticos, direcionando vagas afirmativas e parcerias com ONGs locais de forma estratégica.

## 3. Enquadramento ESG & ODS
* **ODS 8:** Trabalho Decente e Crescimento Econômico (Meta 8.5).
* **ODS 10:** Redução das Desigualdades (Meta 10.2).

## 4. Riscos e Mitigações
* **Risco:** Indisponibilidade de APIs públicas do governo (ex: MTE/CAGED/IBGE) durante o acesso.
* **Mitigação (Fail Gracefully):** Estratégia de Fallback utilizando um arquivo local em cache (`amostra_pcd_uf.json`) na pasta `data/`, garantindo estabilidade à aplicação.

## 5. Cronograma/Fases
* **Fase 1 (TP1):** Escopo, Project Charter, Data Summary Report e App Demo em Streamlit.






