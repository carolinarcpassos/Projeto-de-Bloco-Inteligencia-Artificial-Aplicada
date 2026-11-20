import json
import uuid
from pathlib import Path
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="IncluaTech | Assistente ESG", page_icon="💬", layout="wide")

BASE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = BASE_DIR / "data" / "raw" / "amostra_pcd_uf.json"
CSV_NOTICIAS = BASE_DIR / "data" / "processed" / "noticias_pcd.csv"

if "chat_session_id" not in st.session_state:
    st.session_state.chat_session_id = str(uuid.uuid4())[:8]
if "mensagens_chat" not in st.session_state:
    st.session_state.mensagens_chat = [
        {
            "role": "assistant",
            "content": (
                "Olá! Sou o **Assistente Consultivo ESG do IncluaTech** (conectado via OpenRouter). "
                "Tenho acesso aos indicadores internos de retenção/acessibilidade PcD e às notícias coletadas da Agência Brasil. "
                "O que você gostaria de analisar hoje?"
            )
        }
    ]

with st.sidebar:
    st.title("♿ IncluaTech")
    st.caption("Painel de Governança ESG & Inclusão PcD")
    st.divider()

    st.markdown("### 🔑 Configuração OpenRouter")
    api_key_input = st.text_input(
        "OpenRouter API Key:",
        type="password",
        placeholder="sk-or-v1-...",
        help="Cole sua chave do OpenRouter (openrouter.ai). Ela não fica salva no repositório."
    )
    st.caption(f"ID da Sessão em Memória: `{st.session_state.chat_session_id}`")

    if st.button("🗑️ Limpar Memória da Conversa", use_container_width=True):
        st.session_state.mensagens_chat = [st.session_state.mensagens_chat[0]]
        try:
            requests.delete(f"http://localhost:8000/chat_esg/{st.session_state.chat_session_id}", timeout=5)
        except Exception:
            pass
        st.rerun()

st.title("💬 Assistente Conversacional ESG & Ciclo de Ciência de Dados")
st.caption("Ciclo completo: Coleta (Scraping/JSON) → Classificação BERT Local → Insights Conversacionais com Memória (OpenRouter)")
st.divider()

# =====================================================================
# VISÃO CONSOLIDADA DO CICLO DE CIÊNCIA DE DADOS (DADOS + INSIGHTS)
# =====================================================================
st.markdown("### 🔄 Pipeline de Ciência de Dados Integrado")
col1, col2, col3, col4 = st.columns(4)

total_colab = 0
pct_acess = 0.0
media_retencao = 0.0
if JSON_PATH.exists():
    df_colab = pd.DataFrame(json.loads(JSON_PATH.read_text(encoding="utf-8")))
    total_colab = len(df_colab)
    pct_acess = (len(df_colab[df_colab["Acessibilidade"] == "Sim"]) / total_colab) * 100
    media_retencao = df_colab["Tempo Casa (Meses)"].mean()

total_noticias = 0
if CSV_NOTICIAS.exists():
    df_not = pd.read_csv(CSV_NOTICIAS)
    total_noticias = len(df_not)

col1.metric("1. Dados Internos (JSON)", f"{total_colab} Colaboradores", "Base Estruturada")
col2.metric("2. Web Scraping (Mídia)", f"{total_noticias} Manchetes", "Agência Brasil")
col3.metric("3. Acessibilidade Plena", f"{pct_acess:.1f}%", f"Retenção: {media_retencao:.1f}m")
col4.metric("4. Turnos na Memória", f"{len(st.session_state.mensagens_chat) - 1}", "Contexto Ativo")

with st.expander("📊 Ver Gráfico Comparativo de Retenção Média por Setor"):
    if JSON_PATH.exists():
        resumo_setor = (
            df_colab.groupby("Setor")
            .agg(Tempo_Medio_Casa=("Tempo Casa (Meses)", "mean"))
            .sort_values("Tempo_Medio_Casa", ascending=False)
        )
        st.bar_chart(resumo_setor["Tempo_Medio_Casa"])

st.divider()

# =====================================================================
# INTERFACE CONVERSACIONAL COM MEMÓRIA
# =====================================================================
st.markdown("### 🤖 Converse com os Dados do Projeto")
st.caption("Experimente fazer perguntas em sequência para testar a memória: 1) *'Quais setores têm menor retenção?'* → 2) *'Quais ações de acessibilidade você recomenda para esses setores?'*")

for msg in st.session_state.mensagens_chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt_usuario := st.chat_input("Digite sua pergunta sobre inclusão PcD, retenção ou notícias..."):
    st.session_state.mensagens_chat.append({"role": "user", "content": prompt_usuario})
    with st.chat_message("user"):
        st.markdown(prompt_usuario)

    with st.chat_message("assistant"):
        with st.spinner("Consultando base de dados e histórico da conversa via OpenRouter..."):
            try:
                resp = requests.post(
                    "http://localhost:8000/chat_esg",
                    json={
                        "session_id": st.session_state.chat_session_id,
                        "mensagem": prompt_usuario,
                        "api_key": api_key_input or None
                    },
                    timeout=95
                )
                if resp.status_code == 200:
                    dados_resp = resp.json()
                    resposta_texto = dados_resp["resposta"]
                    st.markdown(resposta_texto)
                    st.caption(
                        f"Fontes consultadas: {', '.join(dados_resp['fontes_utilizadas'])} | "
                        f"Memória ativa: {dados_resp['turnos_na_memoria']} mensagens"
                    )
                    st.session_state.mensagens_chat.append({"role": "assistant", "content": resposta_texto})
                else:
                    erro = resp.json().get("detail", "Erro ao consultar o assistente.")
                    st.error(f"Erro {resp.status_code}: {erro}")
            except requests.exceptions.Timeout:
                st.warning("⏳ O modelo gratuito do OpenRouter demorou mais que o esperado. Envie a pergunta novamente.")
            except requests.exceptions.ConnectionError:
                st.error("🔌 API FastAPI offline (`http://localhost:8000`). Inicie o servidor Uvicorn no terminal.")