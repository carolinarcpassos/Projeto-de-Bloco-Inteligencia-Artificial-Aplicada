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
2. **Entendimento dos Dados (*Data Acquisition and Understanding*):** Coleta via Web Scraping de notícias/portais públicos e dados simulados de recrutamento.
3. **Preparação dos Dados (*Data Preparation*):** Limpeza, tratamento de nulos, contagem de frequência de texto e padronização da CBO e tipos de deficiência.
4. **Modelagem e Aplicação (*Modeling / App Dev*):** Construção do dashboard interativo em Streamlit com cache, filtros, upload de arquivos e nuvem de palavras.
5. **Implantação (*Deployment*):** Publicação no Streamlit Cloud e integração contínua com versionamento Git/GitHub.

---

## 3. Como Executar o Projeto Localmente

Siga as instruções abaixo para configurar o ambiente virtual, instalar as dependências e executar a aplicação em sua máquina.

### Pré-requisitos
* **Python 3.10+** instalado.
* Gerenciador de pacotes **pip** atualizado.

### Passo a Passo de Instalação e Execução

1. **Clonar o repositório:**
   ```bash
   git clone [https://github.com/carolinarcpassos/Projeto-de-Bloco-Inteligencia-Artificial-Aplicada.git](https://github.com/carolinarcpassos/Projeto-de-Bloco-Inteligencia-Artificial-Aplicada.git)
   cd Painel_ODS

---

## 4. Declaração de Uso de Ferramentas de Inteligência Artificial

Em conformidade com as diretrizes acadêmicas do projeto sobre o uso transparente de IA Generativa, declara-se a utilização das seguintes ferramentas como apoio ao desenvolvimento e estudos:

1. **Gemini 2.5 Flash / Gemini 2.0 (Google AI):**
   * **Aplicação:** Assistente de código e arquitetura.
   * **Finalidade:** Suporte na estruturação e otimização de componentes do Streamlit (`st.form`, `st.session_state`, `st.file_uploader`), desenvolvimento do script de Web Scraping (`coleta_web.py`), geração do gráfico de palavras mais frequentes, criação da Nuvem de Palavras (`WordCloud`) e auxílio na documentação metodológica (CRISP-DM/TDSP).

2. **NotebookLM (Google):**
   * **Aplicação:** Ambiente de estudo e síntese de conhecimento.
   * **Finalidade:** Análise, organização de notas e fixação dos conceitos teóricos contidos nas ementas, materiais da disciplina e documentações técnicas do projeto.