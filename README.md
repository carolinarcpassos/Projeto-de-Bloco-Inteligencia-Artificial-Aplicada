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

1. **Entendimento do Negócio (*Business Understanding / Charter*):** Mapeamento de problemas de retenção, definição das métricas ESG e planejamento de integração com LLMs.
2. **Entendimento dos Dados (*Data Acquisition and Understanding*):** Coleta via Web Scraping estático e dinâmico (Selenium), dados de colaboradores e consumo de dados por API REST.
3. **Preparação dos Dados (*Data Preparation*):** Limpeza, extração de texto HTML, filtragem, contagem de frequência e estruturação JSON com validação via Pydantic.
4. **Modelagem e Aplicação (*Modeling / App Dev*):** Construção da interface multipáginas no Streamlit (`pages/`), gráficos interativos, nuvem de palavras, formulários com retenção de estado (`session_state`) e API com FastAPI.
5. **Implantação (*Deployment*):** Publicação no Streamlit Community Cloud, disponibilização da API REST e versionamento com histórico incremental no GitHub.

---

## 3. Estrutura do Repositório

```text
Projeto-de-Bloco-Inteligencia-Artificial-Aplicada/
├── .venv/                      # Ambiente virtual Python
├── api/                        # Serviço de API REST (FastAPI)
│   └── main.py                 # Endpoints GET e POST com validação Pydantic
├── data/                       # Armazenamento de dados
│   ├── processed/              # Dados processados (CSV, TXT)
│   └── raw/                    # Dados brutos (HTML via Selenium, JSON)
├── docs/                       # Documentação técnica do projeto
│   ├── data_summary_report.md  # Relatório sumário dos dados
│   └── project_charter.md      # Project Charter com planejamento de LLMs
├── pages/                      # Páginas do ecossistema multipáginas Streamlit
│   ├── 1_📊_Indicadores.py     # Dashboard analítico e métricas
│   ├── 2_📰_Noticias.py        # Visualizações de scraping e nuvem de palavras
│   └── 3_📥_Ingestao_e_API.py  # Módulo de upload de CSV e documentação da API
├── src/                        # Scripts de raspagem e automação
│   ├── coleta_dinamica.py      # Automação de coleta com Selenium
│   └── coleta_web.py           # Raspagem de dados web
├── Home.py                     # Aplicação principal (Home Page)
├── README.md                   # Documentação do repositório
└── requirements.txt            # Dependências e bibliotecas do projeto
```

---

## 4. Como Executar o Projeto Localmente

Siga as instruções abaixo para configurar o ambiente virtual, instalar as dependências e executar a aplicação em sua máquina.

### Pré-requisitos
* **Python 3.10+** instalado.
* Gerenciador de pacotes **pip** atualizado.
* Google Chrome instalado (necessário para a execução do Selenium WebDriver).

### Passo a Passo de Instalação e Execução

1. **Clonar o repositório:**
   ```bash
   git clone [https://github.com/carolinarcpassos/Projeto-de-Bloco-Inteligencia-Artificial-Aplicada.git](https://github.com/carolinarcpassos/Projeto-de-Bloco-Inteligencia-Artificial-Aplicada.git)
   cd Painel_ODS

2. **Criar e ativar o ambiente virtual:**

python -m venv .venv

# No Linux/macOS: source .venv/bin/activate
# No Windows (PowerShell): .venv\Scripts\Activate.ps1

3. **Instalar as dependências:**

pip install -r requirements.txt

4. **Executar a aplicação Streamlit (Painel Multipáginas):**

streamlit run Home.py

5. **Executar o serviço de API REST (FastAPI - opcional em novo terminal):**

uvicorn api.main:app --reload --port 8000

---

## 5. Declaração de Uso de Ferramentas de Inteligência Artificial

Em conformidade com as diretrizes acadêmicas do projeto sobre o uso transparente de IA Generativa, declara-se a utilização das seguintes ferramentas como apoio ao desenvolvimento e estudos:

1. **Gemini 2.5 Flash / Gemini 2.0 (Google AI):**
   * **Aplicação:** Assistente de código e arquitetura.
   * **Finalidade:** Suporte na estruturação do ambiente multipáginas (pages/), desenvolvimento de endpoints REST com FastAPI e Pydantic, automação de raspagem dinâmica com Selenium (coleta_dinamica.py), refatoração do layout da barra lateral, geração da nuvem de palavras (WordCloud) e padronização dos commits com Conventional Commits.

2. **NotebookLM (Google):**
   * **Aplicação:** Ambiente de estudo e síntese de conhecimento.
   * **Finalidade:** Análise, organização de notas e fixação dos conceitos teóricos contidos nas ementas, materiais da disciplina e documentações técnicas do projeto.