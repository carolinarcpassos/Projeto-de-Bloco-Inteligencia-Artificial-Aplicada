import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="IncluaTech | Painel ODS 8",
    page_icon="♿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Barra lateral da página
with st.sidebar:
    st.title("♿ IncluaTech")
    st.caption("Painel de Governança ESG & Inclusão PcD")
    st.divider()
    
    st.markdown("### 📌 Sumário do Projeto")
    st.markdown("• Contexto & ODS")
    st.markdown("• Métricas de Impacto")
    st.markdown("• Base de Dados (Amostra)")
    st.markdown("• Ecossistema e Links")
    
    st.divider()
    st.info("""
    **Projeto Acadêmico - TP1**  
    Desenvolvido em Python Puro + Streamlit.  
    Alinhado à Agenda 2030 da ONU.
    """)

# Cabeçalho principal 
st.title("♿ IncluaTech: Observatório de Inclusão PcD no Mercado de Trabalho")
st.subheader("Monitoramento analítico de empregabilidade, acessibilidade e retenção de Pessoas com Deficiência")
st.divider()

# Detalhamento do projeto
col_info1, col_info2 = st.columns([2, 1])

with col_info1:
    st.markdown("### 📖 Sobre o Problema de Negócio")
    st.write("""
    Embora a **Lei de Cotas (Lei nº 8.213/1991)** obrigue empresas com mais de 100 funcionários a preencherem de 2% a 5% dos seus cargos com Pessoas com Deficiência (PcD), a inclusão real no mercado brasileiro ainda enfrenta barreiras estruturais severas. 
    
    Frequentemente, o foco das organizações limita-se ao cumprimento formal do percentual legal, negligenciando a **acessibilidade dos postos de trabalho**, a **equidade salarial** e a **plano de carreira**. O resultado é uma alta taxa de rotatividade (*turnover*) e a insatisfação de profissionais qualificados que não encontram ambientes adaptados às suas necessidades (sejam elas físicas, visuais, auditivas ou neurodivergentes).

    **A Solução IncluaTech:**
    O projeto visa centralizar e estruturar dados de empregabilidade PcD, transformando indicadores brutos em diagnósticos claros para equipes de Recursos Humanos, lideranças de ESG e auditores sociais.
    """)

with col_info2:
    st.markdown("### 🎯 Alinhamento ESG & ODS")
    st.success("""
    **ODS 8: Trabalho Decente e Crescimento Econômico**  
    *Meta 8.5:* Alcançar o emprego pleno e produtivo e trabalho decente para todas as pessoas, incluindo pessoas com deficiência, com remuneração igual para trabalho de igual valor.

    **ODS 10: Redução das Desigualdades**  
    *Meta 10.2:* Empoderar e promover a inclusão social, econômica e política de todos, independentemente de deficiência ou outra condição.
    """)

st.divider()

# Cria a tabela de dados sintéticos
@st.cache_data
def load_sample_data():
    return [
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
        {"ID": "PCD-015", "Setor": "Varejo", "Tipo Deficiência": "Intelectual", "Modelo": "Presencial", "Tempo Casa (Meses)": 11, "Acessibilidade": "Sim", "Escolaridade": "Médio Incompleto"},
        {"ID": "PCD-016", "Setor": "Tecnologia", "Tipo Deficiência": "Física/Motora", "Modelo": "Remoto", "Tempo Casa (Meses)": 19, "Acessibilidade": "Sim", "Escolaridade": "Superior Completo"},
        {"ID": "PCD-017", "Setor": "Educação", "Tipo Deficiência": "Visual", "Modelo": "Híbrido", "Tempo Casa (Meses)": 27, "Acessibilidade": "Sim", "Escolaridade": "Mestrado/Doutorado"},
        {"ID": "PCD-018", "Setor": "Logística", "Tipo Deficiência": "Auditiva", "Modelo": "Presencial", "Tempo Casa (Meses)": 4, "Acessibilidade": "Não", "Escolaridade": "Médio Completo"},
        {"ID": "PCD-019", "Setor": "Financeiro", "Tipo Deficiência": "Neurodivergente", "Modelo": "Remoto", "Tempo Casa (Meses)": 16, "Acessibilidade": "Sim", "Escolaridade": "Superior Completo"},
        {"ID": "PCD-020", "Setor": "Saúde", "Tipo Deficiência": "Física/Motora", "Modelo": "Presencial", "Tempo Casa (Meses)": 33, "Acessibilidade": "Parcial", "Escolaridade": "Superior Completo"},
        {"ID": "PCD-021", "Setor": "Tecnologia", "Tipo Deficiência": "Auditiva", "Modelo": "Remoto", "Tempo Casa (Meses)": 13, "Acessibilidade": "Sim", "Escolaridade": "Superior Completo"},
        {"ID": "PCD-022", "Setor": "Indústria", "Tipo Deficiência": "Visual", "Modelo": "Presencial", "Tempo Casa (Meses)": 2, "Acessibilidade": "Não", "Escolaridade": "Médio Incompleto"},
        {"ID": "PCD-023", "Setor": "Varejo", "Tipo Deficiência": "Física/Motora", "Modelo": "Híbrido", "Tempo Casa (Meses)": 29, "Acessibilidade": "Sim", "Escolaridade": "Médio Completo"},
        {"ID": "PCD-024", "Setor": "Financeiro", "Tipo Deficiência": "Múltipla", "Modelo": "Remoto", "Tempo Casa (Meses)": 21, "Acessibilidade": "Parcial", "Escolaridade": "Superior Completo"},
        {"ID": "PCD-025", "Setor": "Tecnologia", "Tipo Deficiência": "Neurodivergente", "Modelo": "Remoto", "Tempo Casa (Meses)": 7, "Acessibilidade": "Sim", "Escolaridade": "Pós-Graduação"},
        {"ID": "PCD-026", "Setor": "Educação", "Tipo Deficiência": "Física/Motora", "Modelo": "Presencial", "Tempo Casa (Meses)": 40, "Acessibilidade": "Sim", "Escolaridade": "Mestrado/Doutorado"},
        {"ID": "PCD-027", "Setor": "Logística", "Tipo Deficiência": "Intelectual", "Modelo": "Presencial", "Tempo Casa (Meses)": 17, "Acessibilidade": "Sim", "Escolaridade": "Médio Completo"},
        {"ID": "PCD-028", "Setor": "Saúde", "Tipo Deficiência": "Visual", "Modelo": "Híbrido", "Tempo Casa (Meses)": 10, "Acessibilidade": "Parcial", "Escolaridade": "Superior Incompleto"},
        {"ID": "PCD-029", "Setor": "Tecnologia", "Tipo Deficiência": "Auditiva", "Modelo": "Remoto", "Tempo Casa (Meses)": 25, "Acessibilidade": "Sim", "Escolaridade": "Superior Completo"},
        {"ID": "PCD-030", "Setor": "Financeiro", "Tipo Deficiência": "Física/Motora", "Modelo": "Híbrido", "Tempo Casa (Meses)": 31, "Acessibilidade": "Sim", "Escolaridade": "Pós-Graduação"}
    ]

dados = load_sample_data()

# Calcula os indicadores
total_registros = len(dados)
remoto_hibrido = sum(1 for d in dados if d["Modelo"] in ["Remoto", "Híbrido"])
acessivel_pleno = sum(1 for d in dados if d["Acessibilidade"] == "Sim")
media_permanencia = sum(d["Tempo Casa (Meses)"] for d in dados) / total_registros

pct_flexivel = (remoto_hibrido / total_registros) * 100
pct_acessivel = (acessivel_pleno / total_registros) * 100

# Exibe os indicadores 
st.markdown("### 📈 Indicadores de Impacto da Amostra")

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric(label="Total de Registros", value=f"{total_registros} Colaboradores")
col_m2.metric(label="Trabalho Flexível", value=f"{pct_flexivel:.1f}%", help="Porcentagem em regime Remoto ou Híbrido")
col_m3.metric(label="Acessibilidade Plena", value=f"{pct_acessivel:.1f}%", help="Vagas com infraestrutura 100% adaptada")
col_m4.metric(label="Tempo Médio de Casa", value=f"{media_permanencia:.1f} Meses", help="Indicador de retenção/turnover")

st.divider()

# Exibe tabela com dados síntéticos
st.markdown("### 📊 Amostra de Dados do Projeto")
st.caption("Visualização da amostra com os 30 registros sintéticos.")

tab_tabela, tab_json = st.tabs(["📋 Tabela Interativa", "🔍 Estrutura JSON"])

with tab_tabela:
    st.dataframe(dados, use_container_width=True, hide_index=True)

with tab_json:
    st.json(dados)

st.divider()

# Fontes de inspiração
st.markdown("### 🔗 Fontes de Inspiração & Ecossistema")

col_link1, col_link2, col_link3 = st.columns(3)

with col_link1:
    st.markdown("**Conecta Brasil**")
    st.write("Plataforma voltada para articulação e transparência de causas sociais.")
    st.link_button("Visitar Conecta Brasil", "https://conectabrasil.org/", use_container_width=True)

with col_link2:
    st.markdown("**Observatório do 3º Setor**")
    st.write("Divulgação de projetos sociais, inclusão e direitos humanos.")
    st.link_button("Visitar Observatório", "https://observatorio3setor.org.br/", use_container_width=True)

with col_link3:
    st.markdown("**Agenda 2030 (ONU)**")
    st.write("Diretrizes oficiais sobre o ODS 8 (Trabalho Decente).")
    st.link_button("Ver ODS 8 na ONU", "https://brasil.un.org/pt-br/sdgs/8", use_container_width=True)

# Rodapé 
st.divider()
st.caption("IncluaTech • Projeto Prático TP1 • Ciência de Dados • 2026")