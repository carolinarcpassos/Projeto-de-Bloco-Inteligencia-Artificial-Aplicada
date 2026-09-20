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