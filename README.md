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

**Justificativa:** Promover a inclusão PcD combate a exclusão socioeconômica, reduz desigualdades e impulsiona o pilar Social (S) da governança ESG[cite: 6].

### Público-Alvo
* Equipes de RH e Gestores de ESG/Diversidade[cite: 6].
* Candidatos e Profissionais PcD[cite: 6].
* Órgãos do Terceiro Setor e Gestores Públicos[cite: 6].

---

## 2. Organização do Projeto (CRISP-DM e TDSP)

1. **Entendimento do Negócio (*Business Understanding / Charter*):** Mapeamento de problemas de retenção, definição das métricas ESG e planejamento de integração com LLMs[cite: 6].
2. **Entendimento dos Dados (*Data Acquisition and Understanding*):** Coleta via Web Scraping estático e dinâmico (Selenium), dados de colaboradores e consumo de dados por API REST[cite: 6].
3. **Preparação dos Dados (*Data Preparation*):** Limpeza, extração de texto HTML, filtragem, contagem de frequência e estruturação JSON com validação via Pydantic[cite: 6].
4. **Modelagem e Aplicação (*Modeling / App Dev & LLM Local*):** Construção da interface multipáginas no Streamlit (`pages/`), gráficos interativos, nuvem de palavras, formulários com retenção de estado (`session_state`), API com FastAPI (`Response Models` e tratamento de exceções HTTP) e integração de modelo LLM local (`nlptown/bert-base-multilingual-uncased-sentiment`) via HuggingFace/PyTorch para classificação de sentimento das notícias PcD[cite: 6, 16].
5. **Implantação (*Deployment*):** Disponibilização local offline do modelo LLM, execução integrada entre API REST e painel Streamlit, e versionamento com histórico incremental no GitHub[cite: 6].

---

## 3. Estrutura do Repositório

```text
Projeto-de-Bloco-Inteligencia-Artificial-Aplicada/
├── .venv/                      # Ambiente virtual Python
├── api/                        # Serviço de API REST (FastAPI + LLM Local)
│   └── main.py                 # Endpoints GET/POST, Response Models, erros HTTP e rota /processar_texto
├── data/                       # Armazenamento de dados
│   ├── processed/              # Dados processados (CSV, TXT)
│   └── raw/                    # Dados brutos (HTML via Selenium, JSON)
├── docs/                       # Documentação técnica do projeto
│   ├── data_summary_report.md  # Relatório sumário dos dados
│   ├── escolha_do_modelo.md    # Critérios de seleção e justificativa do LLM local (TP4)
│   └── project_charter.md      # Project Charter com planejamento e evolução de LLMs
├── pages/                      # Páginas do ecossistema multipáginas Streamlit
│   ├── 1_📊_Indicadores.py     # Dashboard analítico e métricas
│   ├── 2_📰_Noticias.py        # Visualizações de scraping, WordCloud e analisador LLM local
│   └── 3_📥_Ingestao_e_API.py  # Módulo de upload de CSV, documentação e status da API
├── src/                        # Scripts de raspagem, automação e download de modelo
│   ├── baixar_modelo.py        # Download prévio do modelo HuggingFace para o cache local
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

- No Linux/macOS: 
source .venv/bin/activate

- No Windows (PowerShell): 
.venv\Scripts\Activate.ps1

3. **Instalar as dependências:**

pip install -r requirements.txt

4. **Baixar o modelo LLM para o cache local (executar uma vez com internet):**

python src/baixar_modelo.py

5. **Executar o serviço de API REST + LLM Local (FastAPI - Terminal 1):**

uvicorn api.main:app --reload --port 8000

Documentação interativa (Swagger UI): http://localhost:8000/docs
Principais rotas disponíveis:

   GET /: Verifica saúde da API e status de carregamento do modelo LLM.

   GET /colaboradores e POST /colaboradores: Consulta e cadastro de colaboradores PcD.

   POST /processar_texto: Classifica o sentimento e o impacto ESG de manchetes/textos sobre inclusão PcD rodando 100% localmente (local_files_only=True).

6. **Executar a aplicação Streamlit (Painel Multipáginas):**

streamlit run home.py

---

## 5. Declaração de Uso de Ferramentas de Inteligência Artificial

Em conformidade com as diretrizes acadêmicas do projeto sobre o uso transparente de IA Generativa, declara-se a utilização das seguintes ferramentas como apoio ao desenvolvimento e estudos:

1. **Gemini 2.5 Flash / Gemini 2.0 (Google AI):**
   * **Aplicação:** Assistente de código e arquitetura.
   * **Finalidade:** Suporte na estruturação do ambiente multipáginas (pages/), desenvolvimento de endpoints REST com FastAPI e Pydantic (Response Models e exceções HTTP), integração local de modelo HuggingFace (transformers / torch), automação de raspagem dinâmica com Selenium (coleta_dinamica.py), refatoração do layout da barra lateral, geração da nuvem de palavras (WordCloud) e padronização dos commits com Conventional Commits.

2. **NotebookLM (Google):**
   * **Aplicação:** Ambiente de estudo e síntese de conhecimento.
   * **Finalidade:** Análise, organização de notas e fixação dos conceitos teóricos contidos nas ementas, materiais da disciplina e documentações técnicas do projeto.