# Project Charter - IncluaTech (Inclusão PcD no Mercado de Trabalho)

## 1. Visão Geral
* **Nome do Projeto:** IncluaTech - Observatório de Inclusão PcD no Mercado de Trabalho
* **Pergunta Afiada (Sharp Question):** Quais setores econômicos e modelos de trabalho apresentam os maiores déficits de retenção e acessibilidade para pessoas com deficiência (PcD), e como o monitoramento de mídia recente e a gestão de dados internos podem subsidiar decisões estratégicas de RH/ESG?
* **Público-Alvo:** Equipes de Recursos Humanos, Gestores de ESG/Diversidade, Lideranças Corporativas e Profissionais PcD.
* **Cientista de Dados / Desenvolvedora:** Carolina Ramos da Costa Passos.

## 2. Metas e Indicadores de Sucesso (SMART)
* **Entrega Técnica (TP2):** Evoluir a aplicação web analítica interativa no Streamlit, integrando:
  * Ingestão automatizada de notícias via Web Scraping (`coleta_web.py`).
  * Processamento de linguagem natural básico para extração de termos frequentes e geração de Nuvem de Palavras (`WordCloud`).
  * Formulários agrupados de filtragem interativa (`st.form`).
  * Persistência de preferências do usuário por sessão (`st.session_state`).
  * Módulo de Upload de novos dados internos (`st.file_uploader`) e Download de relatórios dinâmicos (`st.download_button`).
  * Otimização de performance através de cache em memória (`@st.cache_data`).
* **Impacto de Negócio:** Reduzir o tempo de diagnóstico de aderência ESG/ODS para equipes de RH e fornecer monitoramento em tempo real do ecossistema de inclusão PcD.

## 3. Enquadramento ESG & ODS
* **ODS 8:** Trabalho Decente e Crescimento Econômico (Meta 8.5 - Alcançar o emprego pleno e produtivo e trabalho decente para todas as pessoas, incluindo pessoas com deficiência).
* **ODS 10:** Redução das Desigualdades (Meta 10.2 - Empoderar e promover a inclusão social, econômica e política de todos, independentemente de deficiência).

## 4. Arquitetura de IA Generativa & Ética Acadêmica
* **Ferramentas de Apoio ao Desenvolvimento:** Gemini (Google AI) e NotebookLM (Google) para auxílio na estruturação de código Python/Streamlit/FastAPI, tratamento de dados e síntese de material didático.
* **Modelo LLM Embarcado na Aplicação (Execução Local):** `nlptown/bert-base-multilingual-uncased-sentiment` (arquitetura BERT multilíngue), carregado offline via `transformers` (`local_files_only=True`) para classificação de sentimento e impacto ESG de notícias PcD.

## 5. Riscos e Mitigações
* **Risco 1:** Indisponibilidade de portais públicos ou alteração na estrutura HTML durante o Web Scraping.
  * **Mitigação:** Tratamento de exceções com blocos `try...except` e fallback para arquivos pré-processados na pasta `data/processed/`.
* **Risco 2:** Recarregamento lento e perda de performance durante interações no dashboard.
  * **Mitigação:** Aplicação do decorator `@st.cache_data` para leitura de dados e isolamento dos filtros em `st.form`.
* **Risco 3:** Indisponibilidade do cache local do modelo LLM ou falha de comunicação entre Streamlit e FastAPI.
  * **Mitigação:** Carregamento único no `lifespan` do FastAPI com retorno padronizado `503 Service Unavailable` caso o modelo não esteja baixado, além de tratamento de `ConnectionError` e `Timeout` na interface Streamlit.

## 6. Arquitetura de Evolução com LLMs
Os dados coletados e estruturados nas etapas anteriores viabilizam as seguintes capacidades de IA na aplicação:
* **Classificação de Sentimentos e Impacto ESG (Implementado na TP4):** Categorização automática do tom das manchetes de notícias (`noticias_pcd.csv`) entre alerta/denúncia, informativo neutro e avanço positivo via modelo BERT local (`POST /processar_texto`).
* **Memória Conversacional e Agentes (Planejado para TP5):** Evolução da aplicação com histórico de contexto e assistente inteligente para apoiar gestores de RH na interpretação dos indicadores de retenção e acessibilidade.

## 7. Cronograma de Evolução
* **Fase 1 (TP1):** Definição do escopo, Project Charter inicial, Data Summary Report preliminar e App Demo básico em Streamlit.
* **Fase 2 (TP2):** Implementação de Web Scraping, filtros interativos com formulário, persistência de estado (`session_state`), geração de nuvem de palavras, caching, upload/download de dados e atualização da documentação técnica.
* **Fase 3 (TP3):** Reestruturação da aplicação em ambiente multipáginas (`pages/`), criação de API REST com FastAPI (endpoints `GET` e `POST`), implementação de Web Scraping dinâmico com Selenium e consolidação do repositório modular.
* **Fase 4 (TP4):** Seleção documentada do modelo LLM local (`docs/escolha_do_modelo.md`), script de cache offline (`src/baixar_modelo.py`), integração do BERT multilíngue na rota `POST /processar_texto` com `Response Models` Pydantic e tratamento robusto de exceções HTTP (`400`, `422`, `500`, `503`), além da integração com a interface Streamlit.
* **Fase 5 (TP5 — Entrega Final):** Consolidação do ciclo completo de Ciência de Dados Aplicada com implementação de **Memória Conversacional e Prompt Engineering via OpenRouter** (`POST /chat_esg`), dashboard interativo final (`pages/4_💬_Assistente_ESG.py`) e fechamento dos artefatos do TSDP (`Data Summary Report` e `Project Charter`), demonstrando como a integração entre dados estruturados, Web Scraping e LLMs subsidia decisões estratégicas de RH e governança ESG.