import streamlit as st

# Configuração global do painel
st.set_page_config(
    page_title="IncluaTech | Home",
    page_icon="♿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Identificação do projeto
with st.sidebar:
    st.title("♿ IncluaTech")
    st.caption("Painel de Governança ESG & Inclusão PcD")
    st.divider()

# Cabeçalho Principal
st.title("♿ IncluaTech: Observatório de Inclusão PcD no Mercado de Trabalho")
st.subheader("Monitorização analítica de empregabilidade, acessibilidade e retenção de Pessoas com Deficiência")
st.divider()

# Informações de Apresentação e Problema de Negócio
col_info1, col_info2 = st.columns([2, 1])

with col_info1:
    st.markdown("### 📖 Sobre o Problema de Negócio")
    st.write("""
    Embora a **Lei de Cotas (Lei nº 8.213/1991)** obrigue empresas com mais de 100 funcionários a preencherem de 2% a 5% dos seus cargos com Pessoas com Deficiência (PcD), a inclusão real no mercado brasileiro ainda enfrenta barreiras estruturais severas. 
    
    Frequentemente, o foco das organizações limita-se ao cumprimento formal do percentual legal, negligenciando a **acessibilidade dos postos de trabalho**, a **equidade salarial** e o **plano de carreira**. O resultado é uma alta taxa de rotatividade (*turnover*) e a insatisfação de profissionais qualificados que não encontram ambientes adaptados às suas necessidades.

    **A Solução IncluaTech:**
    O projeto visa centralizar e estruturar dados de empregabilidade PcD, transformando indicadores brutos em diagnósticos claros para equipas de Recursos Humanos, lideranças de ESG e auditores sociais.
    """)

with col_info2:
    st.markdown("### 🎯 Alinhamento ESG & ODS")
    st.success("""
    **ODS 8: Trabalho Decente e Crescimento Económico**  
    *Meta 8.5:* Alcançar o emprego pleno e produtivo e trabalho decente para todas as pessoas, incluindo pessoas com deficiência, com remuneração igual para trabalho de igual valor.

    **ODS 10: Redução das Desigualdades**  
    *Meta 10.2:* Empoderar e promover a inclusão social, económica e política de todos, independentemente de deficiência ou outra condição.
    """)

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

st.divider()
st.info("👈 **Navegação:** Utiliza o menu lateral para navegar entre as páginas de **Indicadores**, **Notícias** e **Ingestão & API**.")
st.caption("IncluaTech • Projeto Prático TP3 • Ciência de Dados • 2026")