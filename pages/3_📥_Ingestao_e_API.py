import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="IncluaTech | Ingestão e API", page_icon="📥", layout="wide")

# Identificação do projeto
with st.sidebar:
    st.title("♿ IncluaTech")
    st.caption("Painel de Governança ESG & Inclusão PcD")
    st.divider()

st.title("📥 Ingestão de Dados & Integração com API")
st.divider()

st.markdown("### 1. Serviço de Upload e Gestão de Dados Internos")
arquivo_upload = st.file_uploader("Selecione um arquivo CSV com novos dados:", type=["csv"])

if arquivo_upload is not None:
    try:
        df_uploaded = pd.read_csv(arquivo_upload)
        st.success("Ficheiro carregado com sucesso!")
        st.dataframe(df_uploaded.head(5), use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao processar o ficheiro enviado: {e}")

st.divider()

st.markdown("### 2. Integração via API REST (FastAPI & LLM Local)")
st.write("""
A aplicação possui um serviço autónomo de **API REST** desenvolvido em FastAPI para consulta/envio de registos e análise inteligente de textos com modelo LLM rodando localmente (HuggingFace).

* **URL Local do Servidor:** `http://localhost:8000`
* **Documentação Interativa (Swagger UI):** [Acessar /docs](http://localhost:8000/docs)
* **Rotas Disponíveis:**
  * `GET /`: Verifica o status da API e se o modelo LLM local está carregado na memória.
  * `GET /colaboradores`: Consulta toda a base de colaboradores.
  * `POST /colaboradores`: Regista um novo colaborador na base JSON.
  * `POST /processar_texto`: Processa manchetes ou textos sobre inclusão PcD utilizando o modelo BERT local (`nlptown/bert-base-multilingual-uncased-sentiment`) e retorna a classificação de impacto ESG validada via *Response Model
  * `POST /chat_esg`: Assistente conversacional ESG com memória de sessão via OpenRouter e *grounding* nos dados reais do projeto.*.
""")

if st.button("Verificar Status da API e do Modelo LLM"):
    try:
        resp = requests.get("http://localhost:8000/", timeout=5)
        if resp.status_code == 200:
            info = resp.json()
            if info.get("llm_carregado"):
                st.success("✅ API online e modelo LLM local carregado com sucesso!")
            else:
                st.warning("⚠️ API online, mas o modelo LLM não está carregado (erro 503 será retornado nas análises). Execute `python src/baixar_modelo.py`.")
        else:
            st.error(f"❌ A API respondeu com status inesperado: {resp.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("🔌 Não foi possível conectar em `http://localhost:8000`. Certifique-se de rodar o Uvicorn no terminal.")

st.info("💡 **Dica:** Certifique-se de executar `uvicorn api.main:app --reload --port 8000`  em outro terminal para que a API fique acessível.")