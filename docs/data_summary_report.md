# Data Summary Report - IncluaTech (Evolução TP2)

## 1. Fontes de Dados e Artefatos do Projeto

| Fonte / Artefato | Tipo de Dado | Acesso / Método | Localização / Arquivo | Objetivo e Uso na Aplicação |
| :--- | :--- | :--- | :--- | :--- |
| **Portal Agência Brasil / Notícias PcD** | Não Estruturado (Texto / HTML) | Web Scraping (`BeautifulSoup` + `requests`) | `src/coleta_web.py` $\rightarrow$ `data/processed/noticias_pcd.csv` | Capturar manchetes e links recentes sobre PcD para análise de termos frequentes e geração da Nuvem de Palavras. |
| **Base de Amostra Institucional** | Estruturado | Leitura de arquivo local | `data/processed/` / Simulada via DataFrame | Alimentar o painel principal com indicadores de colaboradores (setor, modelo de trabalho, acessibilidade, tempo de casa). |
| **Upload de Dados do Usuário** | Estruturado (CSV) | Upload dinâmico (`st.file_uploader`) | Memória da Sessão (`Pandas DataFrame`) | Permitir que gestores de RH façam a carga de novas bases de colaboradores para diagnóstico imediato. |
| **Relatório Consolidado Filtrado** | Estruturado (CSV) | Exportação dinâmica (`st.download_button`) | Gerado sob demanda (`relatorio_incluatech_pcd.csv`) | Permitir a exportação dos dados filtrados no painel para análise externa em planilhas ou relatórios de ESG. |

---

## 2. Pipeline de Processamento e Transformação de Dados

1. **Coleta e Extração (`coleta_web.py`):**
   * Faz requisições HTTP para a editoria de Direitos Humanos da Agência Brasil.
   * Extrai títulos de notícias contendo palavras-chave relacionadas à inclusão PcD.
   * Persiste os resultados em formato estruturado (`noticias_pcd.csv`) e em texto bruto (`noticias_pcd.txt`).

2. **Limpeza e Processamento de Texto (NLP Básico em `app.py`):**
   * Tokenização simples das manchetes coletadas.
   * Remoção de *stopwords* (palavras irrelevantes como "de", "em", "para", "com", "são", "diz").
   * Contagem de frequência absoluta utilizando `collections.Counter` para gráfico de barras.
   * Construção visual da matriz de frequência via `WordCloud` e renderização via `matplotlib.pyplot`.

3. **Filtragem e Gestão de Estado:**
   * Agrupamento das opções de filtro por *Setor de Trabalho* e *Modelo de Trabalho* via `st.form`.
   * Filtragem de alta performance no DataFrame através do Pandas.
   * Salvamento e exibição de setores favoritados pelo usuário via `st.session_state`.

---

## 3. Qualidade, Desafios e Boas Práticas

* **Otimização e Caching:** Utilização do decorator `@st.cache_data` na função de carregamento da amostragem, evitando releituras do disco a cada renderização da interface.
* **Tratamento de Exceções:** Implementação de blocos `try...except` na leitura de arquivos enviados via upload e na abertura de fontes de dados, garantindo mensagens claras ao usuário final (`st.error`).
* **Privacidade e LGPD:** A base de dados opera exclusivamente com identificadores genéricos (`PCD-101`, `PCD-102`), sem exposição de dados pessoais sensíveis (PII).

---

## 4. Novas Fontes e Fluxos de Dados (TP3)

### 4.1. Coleta Dinâmica via Selenium (Dados Brutos)
- **Origem:** Raspagem dinâmica de dados do portal Agência Brasil (Direitos Humanos).
- **Arquivo Salvo:** `data/raw/pagina_dinamica.html`
- **Formato:** HTML bruto (snapshot da página carregada via JavaScript).
- **Finalidade:** Servir de base para o processamento e extração de notícias com BeautifulSoup (`data/processed/noticias_pcd.csv`).

### 4.2. Endpoints da API REST (FastAPI)
- **Base de Dados:** `amostra_pcd_uf.json`
- **Estrutura dos Dados Trafegados (Schema Pydantic):**
  - `ID` (string): Identificador único do colaborador.
  - `Setor` (string): Setor de atuação (ex: Tecnologia, Varejo, Saúde).
  - `Tipo_Deficiencia` (string): Tipo de deficiência declarada.
  - `Modelo` (string): Modelo de trabalho (Remoto, Híbrido, Presencial).
  - `Tempo_Casa_Meses` (inteiro): Tempo de permanência na empresa em meses.
  - `Acessibilidade` (string): Nível de acessibilidade do posto (Sim, Parcial, Não).
  - `Escolaridade` (string): Grau de instrução do colaborador.
- **Rotas:**
  - `GET /colaboradores`: Retorna a lista completa de colaboradores em formato JSON.
  - `POST /colaboradores`: Recebe um payload JSON no formato do schema acima para cadastrar um novo registro.

---

## 5. Consolidação do Ciclo de Dados e Integração com LLMs (TP4 e TP5)

### 5.1. Pipeline Ponta a Ponta de Ciência de Dados
1. **Coleta (TP2/TP3):** Extração automatizada de manchetes da Agência Brasil via `BeautifulSoup` (`src/coleta_web.py`) e `Selenium` (`src/coleta_dinamica.py`), combinada à base estruturada de colaboradores (`amostra_pcd_uf.json`).
2. **Enriquecimento Semântico Local (TP4):** Classificação automática das manchetes por meio do modelo BERT multilíngue (`nlptown/bert-base-multilingual-uncased-sentiment`) executado localmente via FastAPI (`POST /processar_texto`), categorizando notícias em *Alerta/Denúncia*, *Neutro/Informativo* ou *Avanço Positivo*.
3. **Síntese Conversacional e Apoio à Decisão (TP5):** Injeção dinâmica das métricas agregadas de `amostra_pcd_uf.json` (retenção por setor, taxa de acessibilidade, modelos de trabalho) e das manchetes de `data/processed/noticias_pcd.csv` no *System Prompt* do endpoint `POST /chat_esg` (integrado via OpenRouter), permitindo consultas contínuas com memória conversacional no painel Streamlit (`pages/4_💬_Assistente_ESG.py`).

### 5.2. Principais Insights Extraídos dos Dados Reais do Projeto
* **Correlação entre Acessibilidade e Retenção:** Colaboradores em postos com acessibilidade plena (`Sim`) ou modelo flexível (`Remoto`/`Híbrido`, predominantes em Tecnologia e Financeiro) apresentam maior estabilidade, enquanto setores presenciais sem adaptação (`Logística` e `Indústria`) concentram casos críticos de baixa permanência (entre 2 e 8 meses).
* **Panorama Midiático:** As manchetes coletadas evidenciam sub-representação de PcDs em cargos de liderança (apenas 1,5% das vagas) e barreiras estruturais, reforçando a urgência de políticas internas alinhadas aos ODS 8 e 10.