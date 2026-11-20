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
* Candidatos e Profissionais PcD
* Órgãos do Terceiro Setor e Gestores Públicos.

---

## 2. Organização do Projeto (CRISP-DM e TDSP)

1. **Entendimento do Negócio (*Business Understanding / Charter*):** Mapeamento de problemas de retenção, definição das métricas ESG e planejamento de integração com LLMs.
2. **Entendimento dos Dados (*Data Acquisition and Understanding*):** Coleta via Web Scraping estático e dinâmico (Selenium), dados de colaboradores e consumo de dados por API REST.
3. **Preparação dos Dados (*Data Preparation*):** Limpeza, extração de texto HTML, filtragem, contagem de frequência e estruturação JSON com validação via Pydantic.
4. **Modelagem e Aplicação (*Modeling / App Dev & LLM Local*):** Construção da interface multipáginas no Streamlit (`pages/`), gráficos interativos, nuvem de palavras, formulários com retenção de estado (`session_state`), API com FastAPI (`Response Models` e tratamento de exceções HTTP) e integração de modelo LLM local (`nlptown/bert-base-multilingual-uncased-sentiment`) via HuggingFace/PyTorch para classificação de sentimento das notícias PcD.
5. **Implantação (*Deployment*):** Disponibilização local offline do modelo LLM, execução integrada entre API REST e painel Streamlit, e versionamento com histórico incremental no GitHub.

---

## 3. Estrutura do Repositório

```text
Projeto-de-Bloco-Inteligencia-Artificial-Aplicada/
├── .venv/                       # Ambiente virtual Python
├── api/                         # Serviço de API REST (FastAPI + LLMs)
│   └── main.py                  # Endpoints CRUD, BERT local (/processar_texto) e Chat ESG (/chat_esg)
├── data/                        # Armazenamento de dados
│   ├── processed/               # Dados processados (noticias_pcd.csv, noticias_pcd.txt)
│   └── raw/                     # Dados brutos (HTML via Selenium)
├── docs/                        # Artefatos do TDSP e documentação técnica
│   ├── data_summary_report.md   # Relatório sumário dos dados e consolidação do pipeline
│   ├── escolha_do_modelo.md     # Critérios de seleção e justificativa do modelo BERT local
│   ├── integracao_llm_api.md    # Arquitetura da API, Response Models e matriz de erros HTTP
│   └── project_charter.md       # Project Charter com escopo, riscos e cronograma completo
├── pages/                       # Páginas do ecossistema multipáginas Streamlit
│   ├── 1_📊_Indicadores.py      # Dashboard analítico de retenção e acessibilidade PcD
│   ├── 2_📰_Noticias.py         # Visualizações de scraping, WordCloud e classificador BERT local
│   ├── 3_📥_Ingestao_e_API.py   # Upload de CSV, documentação e verificação de status da API
│   └── 4_💬_Assistente_ESG.py   # Dashboard final com pipeline integrado e chat ESG com memória
├── src/                         # Scripts de raspagem e cache offline de modelo
│   ├── baixar_modelo.py         # Download prévio do modelo HuggingFace para o cache local
│   ├── coleta_dinamica.py       # Automação de coleta com Selenium
│   └── coleta_web.py            # Raspagem de dados web com BeautifulSoup
├── amostra_pcd_uf.json          # Base estruturada de colaboradores PcD
├── Home.py                      # Aplicação principal (Home Page)
├── README.md                    # Documentação geral do repositório
└── requirements.txt             # Dependências e bibliotecas do projeto
```

---

## 4. Como Executar o Projeto Localmente

Siga as instruções abaixo para configurar o ambiente virtual, instalar as dependências e executar a aplicação em sua máquina.

### Pré-requisitos
* **Python 3.10+** instalado.
* Gerenciador de pacotes **pip** atualizado.
* Google Chrome instalado (necessário para a execução do Selenium WebDriver).
* Chave de API gratuita do OpenRouter (https://openrouter.ai) para ativar as respostas generativas completas no Assistente ESG (caso não seja informada, a aplicação opera em modo analítico de contingência usando os dados locais).

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

   POST /chat_esg e DELETE /chat_esg/{session_id}: Assistente conversacional ESG com memória de sessão via OpenRouter e grounding automático nos dados internos e raspados.

6. **Executar a aplicação Streamlit (Painel Multipáginas):**

streamlit run home.py
Acesse no navegador: http://localhost:8501

Na página 💬 Assistente ESG, insira sua OpenRouter API Key na barra lateral e interaja com o chat para obter análises contextualizadas sobre retenção, acessibilidade e notícias PcD.

---

## 5. Declaração de Uso de Ferramentas de Inteligência Artificial

Em conformidade com as diretrizes acadêmicas do projeto sobre o uso transparente de IA Generativa, declara-se a utilização das seguintes ferramentas como apoio ao desenvolvimento e estudos:

1. **Gemini 2.5 Flash / Gemini 2.0 (Google AI):**
   * **Aplicação:** Assistente de código e arquitetura.
   * **Finalidade:** Suporte na estruturação do ambiente multipáginas (pages/), desenvolvimento de endpoints REST com FastAPI e Pydantic (Response Models e exceções HTTP), integração local de modelo HuggingFace (transformers / torch), automação de raspagem dinâmica com Selenium (coleta_dinamica.py), refatoração do layout da barra lateral, geração da nuvem de palavras (WordCloud) implementação da memória conversacional e Prompt Engineering no assistente ESG, além da padronização dos artefatos TSDP e commits semânticos.

2. **OpenRouter (openrouter/free):
   * **Aplicação:** Infraestrutura de inferência LLM integrada à aplicação na TP5.
   * **Finalidade:** Processamento das interações em linguagem natural no endpoint POST /chat_esg, sintetizando indicadores internos de RH e notícias raspadas com manutenção de contexto conversacional.

3. **NotebookLM (Google):**
   * **Aplicação:** Ambiente de estudo e síntese de conhecimento.
   * **Finalidade:** Análise, organização de notas e fixação dos conceitos teóricos contidos nas ementas, materiais da disciplina e documentações técnicas do projeto.