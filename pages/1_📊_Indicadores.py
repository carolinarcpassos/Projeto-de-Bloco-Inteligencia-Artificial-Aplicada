import streamlit as st
import pandas as pd

st.set_page_config(page_title="IncluaTech | Indicadores", page_icon="📊", layout="wide")

# Gerenciamento de estado para favoritos
if "setores_favoritos" not in st.session_state:
    st.session_state.setores_favoritos = []

# Carregamento de dados em cache
@st.cache_data
def load_sample_data():
    return pd.DataFrame([
        {"ID": "PCD-001", "Setor": "Tecnologia", "Tipo Deficiência": "Visual", "Modelo": "Remoto", "Tempo Casa (Meses)": 14, "Acessibilidade": "Sim", "Escolaridade": "Superior Completo"},
        {"ID": "PCD-002", "Setor": "Financeiro", "Tipo Deficiência": "Física/Motora", "Modelo": "Híbrido", "Tempo Casa (Meses)": 6, "Acessibilidade": "Parcial", "Escolaridade": "Pós-Graduação"},
        {"ID": "PCD-003", "Setor": "Varejo", "Tipo Deficiência": "Auditiva", "Modelo": "Presencial", "Tempo Casa (Meses)": 24, "Acessibilidade": "Sim", "Escolaridade": "Médio Completo"},
        {"ID": "PCD-004", "Setor": "Tecnologia", "Tipo Deficiência": "Neurodivergente", "Modelo": "Remoto", "Tempo Casa (Meses)": 3, "Acessibilidade": "Sim", "Escolaridade": "Superior Completo"},
        {"ID": "PCD-005", "Setor": "Saúde", "Tipo Deficiência": "Múltipla", "Modelo": "Presencial", "Tempo Casa (Meses)": 36, "Acessibilidade": "Não", "Escolaridade": "Médio Incompleto"},
        {"ID": "PCD-006", "Setor": "Varejo", "Tipo Deficiência": "Física/Motora", "Modelo": "Híbrido", "Tempo Casa (Meses)": 12, "Acessibilidade": "Sim", "Escolaridade": "Médio Completo"},
        {"ID": "PCD-007", "Setor": "Educação", "Tipo Deficiência": "Auditiva", "Modelo": "Presencial", "Tempo Casa (Meses)": 18, "Acessibilidade": "Parcial", "Escolaridade": "Superior Completo"},
        {"ID": "PCD-008", "Setor": "Financeiro", "Tipo Deficiência": "Visual", "Modelo": "Remoto", "Tempo Casa (Meses)": 9, "Acessibilidade": "Sim", "Escolaridade": "Pós-Graduação"},
        {"ID": "PCD-009", "Setor": "Tecnologia", "Tipo Deficiência": "Neurodivergente", "Modelo": "Remoto", "Tempo Casa (Meses)": 30, "Acessibilidade": "Sim", "Escolaridade": "Superior Completo"},
        {"ID": "PCD-010", "Setor": "Saúde", "Tipo Deficiência": "Física/Motora", "Modelo": "Híbrido", "Tempo Casa (Meses)": 15, "Acessibilidade": "Sim", "Escolaridade": "Superior Incompleto"},
        {"ID": "PCD-011", "Setor": "Logística", "Tipo Deficiência": "Auditiva", "Modelo": "Presencial", "Tempo Casa (Meses)": 8, "Acessibilidade": "Não", "Escolaridade": "Médio Completo"},
        {"ID": "PCD-012", "Setor": "Tecnologia", "Tipo Deficiência": "Visual", "Modelo": "Remoto", "Tempo Casa (Meses)": 22, "Acessibilidade": "Sim", "Escolaridade": "Pós-Graduação"},
        {"ID": "PCD-013", "Setor": "Financeiro", "Tipo Deficiência": "Neurodivergente", "Modelo": "Híbrido", "Tempo Casa (Meses)": 5, "Acessibilidade": "Sim", "Escolaridade": "Superior Completo"},
        {"ID": "PCD-014", "Setor": "Indústria", "Tipo Deficiência": "Física/Motora", "Modelo": "Presencial", "Tempo Casa (Meses)": 48, "Acessibilidade": "Parcial", "Escolaridade": "Médio Completo"},
        {"ID": "PCD-015", "Setor": "Varejo", "Tipo Deficiência": "Intelectual", "Modelo": "Presencial", "Tempo Casa (Meses)": 11, "Acessibilidade": "Sim", "Escolaridade": "Médio Incompleto"}
    ])

df_dados = load_sample_data()

# Barra lateral de filtros
with st.sidebar:
    st.title("♿ IncluaTech")
    st.caption("Painel de Governança ESG & Inclusão PcD")
    st.divider()
    
    with st.form("form_filtros_interativos"):
        st.markdown("### ⚙️ Filtros do Painel")
        setores_disponiveis = df_dados["Setor"].unique().tolist()
        setores_sel = st.multiselect("Filtrar por Setor de Trabalho:", setores_disponiveis, default=setores_disponiveis)
        
        modelos_disponiveis = df_dados["Modelo"].unique().tolist()
        modelos_sel = st.multiselect("Filtrar por Modelo de Trabalho:", modelos_disponiveis, default=modelos_disponiveis)
        
        st.form_submit_button("Aplicar Filtros")

    st.divider()
    st.markdown("### ⭐ Favoritar Sessão")
    setor_fav = st.selectbox("Escolha um Setor para favoritar:", setores_disponiveis)
    if st.button("Favoritar Setor"):
        if setor_fav not in st.session_state.setores_favoritos:
            st.session_state.setores_favoritos.append(setor_fav)
            st.success(f"Setor {setor_fav} adicionado aos favoritos!")

    if st.session_state.setores_favoritos:
        st.write("**Seus favoritos:**", ", ".join(st.session_state.setores_favoritos))

# Aplicação dos Filtros
df_filtrado = df_dados[
    (df_dados["Setor"].isin(setores_sel)) & 
    (df_dados["Modelo"].isin(modelos_sel))
]

st.title("📊 Indicadores de Impacto & Governança PcD")
st.divider()

total_registros = len(df_filtrado)

if total_registros > 0:
    remoto_hibrido = len(df_filtrado[df_filtrado["Modelo"].isin(["Remoto", "Híbrido"])])
    acessivel_pleno = len(df_filtrado[df_filtrado["Acessibilidade"] == "Sim"])
    media_permanencia = df_filtrado["Tempo Casa (Meses)"].mean()

    pct_flexivel = (remoto_hibrido / total_registros) * 100
    pct_acessivel = (acessivel_pleno / total_registros) * 100

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric(label="Total de Registos", value=f"{total_registros} Colaboradores")
    col_m2.metric(label="Trabalho Flexível", value=f"{pct_flexivel:.1f}%")
    col_m3.metric(label="Acessibilidade Plena", value=f"{pct_acessivel:.1f}%")
    col_m4.metric(label="Tempo Médio de Casa", value=f"{media_permanencia:.1f} Meses")
    
    st.divider()
    
    st.markdown("### 📊 Amostra de Dados do Projeto")
    tab_tabela, tab_json = st.tabs(["📋 Tabela Interativa", "🔍 Estrutura JSON"])
    with tab_tabela:
        st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
    with tab_json:
        st.json(df_filtrado.to_dict(orient="records"))

    st.markdown("#### 📤 Exportar Relatório Personalizado")
    csv_export = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="💾 Baixar Dados Filtrados (CSV)",
        data=csv_export,
        file_name="relatorio_incluatech_pcd.csv",
        mime="text/csv"
    )
else:
    st.warning("Nenhum registo encontrado para a combinação de filtros selecionada.")