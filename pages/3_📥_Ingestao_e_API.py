import streamlit as st
import pandas as pd

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

st.markdown("### 2. Integração via API REST (FastAPI)")
st.write("""
A aplicação possui um serviço autónomo de **API REST** desenvolvido em FastAPI para consulta e envio automatizado de registos.

* **URL Local do Servidor:** `http://localhost:8000`
* **Documentação Interativa (Swagger UI):** [Acessar /docs](http://localhost:8000/docs)
* **Rotas Disponíveis:**
  * `GET /colaboradores`: Consulta toda a base de colaboradores.
  * `POST /colaboradores`: Regista um novo colaborador na base JSON.
""")

st.info("💡 **Dica:** Certifica-te de que executaste `uvicorn api.main:app --reload --port 8000` noutro terminal para que a API fique acessível.")