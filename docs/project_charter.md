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
* **Ferramentas:** Gemini 2.5 Flash / Gemini 2.0 (Google AI) e NotebookLM (Google).
* **Escopo de Uso:** Auxílio na estruturação de código Python/Streamlit, refatoração de componentes visuais, lógica de tratamento de dados com Pandas e síntese de material didático de suporte.

## 5. Riscos e Mitigações
* **Risco 1:** Indisponibilidade de portais públicos ou alteração na estrutura HTML durante o Web Scraping.
* **Mitigação:** Tratamento de exceções com blocos `try...except` e fallback para arquivos pré-processados na pasta `data/processed/`.
* **Risco 2:** Recarregamento lento e perda de performance durante interações do usuário no dashboard.
* **Mitigação:** Aplicação do decorator `@st.cache_data` para leitura de dados e isolamento dos filtros em `st.form`.

## 7. Preparação para Uso de LLMs (Próxima Fase)
Os dados coletados nesta etapa foram estruturados para viabilizar as seguintes aplicações com Large Language Models:
* **Classificação de Sentimentos:** Categorização do tom das manchetes de notícias (`noticias_pcd.csv`) em positivo, neutro ou denúncia.
* **Resumo Automático:** Geração de relatórios executivos narrativos sobre o nível de acessibilidade com base nos indicadores.
* **Sistema de Perguntas e Respostas (Q&A / RAG):** Assistente inteligente para tirar dúvidas sobre cotas e acessibilidade.

## 6. Cronograma de Evolução
* **Fase 1 (TP1):** Definição do escopo, Project Charter inicial, Data Summary Report preliminar e App Demo básico em Streamlit.
* **Fase 2 (TP2):** Implementação de Web Scraping, filtros interativos com formulário, persistência de estado (`session_state`), geração de nuvem de palavras, caching, upload/download de dados e atualização da documentação técnica.
* **Fase 3 (TP3):** Reestruturação da aplicação em ambiente multipáginas (`pages/`), criação de API REST com FastAPI (endpoints `GET` e `POST`), implementação de Web Scraping dinâmico com Selenium, consolidação do repositório modular e atualização da documentação estratégica para integração com LLMs.
