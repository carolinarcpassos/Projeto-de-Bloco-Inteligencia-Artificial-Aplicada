# IncluaTech: Painel de Monitoramento e Match Inteligente para Inclusão PcD

## 1. Identificação do Problema de Negócio

### Definição do Problema
Apesar da Lei de Cotas (Lei nº 8.213/1991) no Brasil, as empresas frequentemente enfrentam dificuldades para atrair, integrar e reter talentos com deficiência (PcD). Por outro lado, profissionais PcD enfrentam barreiras de acessibilidade no recrutamento e incompatibilidade de cargos. Há escassez de análises de dados sobre retenção, acessibilidade real e equidade de oportunidades.

### Metas e Indicadores de Sucesso (KPIs)
* **Meta Principal:** Desenvolver uma aplicação analítica para diagnosticar o nível de inclusão PcD e otimizar processos de atração e retenção no mercado corporativo.
* **Indicadores de Sucesso (KPIs):**
  1. **Taxa de Conformidade à Lei de Cotas:** Porcentagem do cumprimento das cotas por setor e empresa.
  2. **Índice de Retenção (Turnover PcD):** Medição da permanência dos colaboradores PcD nos primeiros 12 meses.
  3. **Métrica de Acessibilidade das Vagas:** Proporção de vagas ofertadas com adaptações comprovadas (remoto, LIBRAS, acessibilidade física).

### Alinhamento aos Objetivos de Desenvolvimento Sustentável (ODS)
* **ODS 8: Trabalho Decente e Crescimento Econômico** (Meta 8.5: Trabalho decente e igualdade de remuneração para pessoas com deficiência).
* **ODS 10: Redução das Desigualdades** (Meta 10.2: Promover a inclusão social, econômica e política de todos).

**Justificativa:** Promover a inclusão PcD combate a exclusão socioeconômica, reduz desigualdades e impulsiona o pilar Social (S) da governança ESG.

### Público-Alvo
* Equipes de RH e Gestores de ESG/Diversidade.
* Candidatos e Profissionais PcD.
* Órgãos do Terceiro Setor e Gestores Públicos.

---

## 2. Organização do Projeto (CRISP-DM e TDSP)

1. **Entendimento do Negócio (*Business Understanding / Charter*):** Mapeamento de problemas de retenção e definição das métricas ESG.
2. **Entendimento dos Dados (*Data Acquisition and Understanding*):** Coleta via API de dados públicos (RAIS/CAGED, IBGE) e simulados de recrutamento.
3. **Preparação dos Dados (*Data Preparation*):** Limpeza, tratamento de nulos e padronização da CBO e tipos de deficiência.
4. **Modelagem e Aplicação (*Modeling / App Dev*):** Construção do dashboard interativo em Streamlit.
5. **Implantação (*Deployment*):** Publicação no Streamlit Cloud e entrega de artefatos no GitHub.