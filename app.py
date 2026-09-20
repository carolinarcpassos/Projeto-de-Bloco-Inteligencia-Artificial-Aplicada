# Importação das bibliotecas que serão usadas
import streamlit as st
import pandas as pd
import csv
from collections import Counter
from pathlib import Path
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Define o caminho base do projeto de forma dinâmica
BASE_DIR = Path(__file__).resolve().parent

# Configuração da página
st.set_page_config(
    page_title="IncluaTech | Painel ODS 8",
    page_icon="♿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Gerenciamento de estado da sessão
if "setores_favoritos" not in st.session_state:
    st.session_state.setores_favoritos = []

# Carrega e armazena em cache os dados síntéticos para ganho de performance
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
    ])

df_dados = load_sample_data()


# Barra lateral da página e formulário de filtros dinâmicos
with st.sidebar:
     st.title("♿ IncluaTech")
     st.caption("#### Painel de Governança ESG & Inclusão PcD")
     st.divider()
    
     # Agrupamento de filtros em formulário para otimização
     with st.form("form_filtros_interativos"):
          st.markdown("### ⚙️ Filtros do Painel")
        
          setores_disponiveis = df_dados["Setor"].unique().tolist()
          setores_sel = st.multiselect("Filtrar por Setor de Trabalho:", setores_disponiveis, default=setores_disponiveis)
        
          modelos_disponiveis = df_dados["Modelo"].unique().tolist()
          modelos_sel = st.multiselect("Filtrar por Modelo de Trabalho:", modelos_disponiveis, default=modelos_disponiveis)
        
          btn_aplicar = st.form_submit_button("Aplicar Filtros")

     st.divider()

     # Funcionalidade de favoritar 
     st.markdown("### ⭐ Favoritar Sessão")
     setor_fav = st.selectbox("Escolha um Setor de Trabalho para favoritar:", setores_disponiveis)
     if st.button("Favoritar Setor"):
          if setor_fav not in st.session_state.setores_favoritos:
             st.session_state.setores_favoritos.append(setor_fav)
             st.success(f"Setor {setor_fav} adicionado aos favoritos!")

     if st.session_state.setores_favoritos:
        st.write("**Seus favoritos:**", ", ".join(st.session_state.setores_favoritos))

     st.divider()
     st.info("""
     **Projeto Acadêmico - TP2**  
     Desenvolvido em Python + Streamlit.  
     Integrado a Web Scraping e Caching.  
     *Suporte de IA Generativa: Gemini 2.5 Flash / Gemini 2.0 (Google AI) +
     NotebookLM (Google).*
     """)

# Aplicação dos filtros sobre o DataFrame
df_filtrado = df_dados[
    (df_dados["Setor"].isin(setores_sel)) & 
    (df_dados["Modelo"].isin(modelos_sel))
]

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

# Indicadores de impacto dinâmicos (Calculados sobre o DF Filtrado)
st.markdown("### 📈 Indicadores de Impacto da Amostra Filtrada")

total_registros = len(df_filtrado)

if total_registros > 0:
    remoto_hibrido = len(df_filtrado[df_filtrado["Modelo"].isin(["Remoto", "Híbrido"])])
    acessivel_pleno = len(df_filtrado[df_filtrado["Acessibilidade"] == "Sim"])
    media_permanencia = df_filtrado["Tempo Casa (Meses)"].mean()

    pct_flexivel = (remoto_hibrido / total_registros) * 100
    pct_acessivel = (acessivel_pleno / total_registros) * 100

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric(label="Total de Registros", value=f"{total_registros} Colaboradores")
    col_m2.metric(label="Trabalho Flexível", value=f"{pct_flexivel:.1f}%", help="Porcentagem em regime Remoto ou Híbrido")
    col_m3.metric(label="Acessibilidade Plena", value=f"{pct_acessivel:.1f}%", help="Vagas com infraestrutura 100% adaptada")
    col_m4.metric(label="Tempo Médio de Casa", value=f"{media_permanencia:.1f} Meses", help="Indicador de retenção/turnover")
else:
    st.warning("Nenhum registro encontrado para a combinação de filtros selecionada na barra lateral.")

st.divider()

# Visualização e Serviço de Download
st.markdown("### 📊 Amostra de Dados do Projeto")
st.caption("Visualização dos registros filtrados e serviço de exportação de relatórios.")

tab_tabela, tab_json = st.tabs(["📋 Tabela Interativa", "🔍 Estrutura JSON"])

with tab_tabela:
    st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

with tab_json:
    st.json(df_filtrado.to_dict(orient="records"))

# Botão de Download do relatório filtrado
st.markdown("#### 📤 Exportar Relatório Customizado")
csv_export = df_filtrado.to_csv(index=False).encode('utf-8')
st.download_button(
    label="💾 Baixar Dados Filtrados (CSV)",
    data=csv_export,
    file_name="relatorio_incluatech_pcd.csv",
    mime="text/csv"
)

st.divider()

# Exibição dos dados extraídos da Web (Web Scraping / Beautiful Soup)
st.markdown("### 📰 Monitoramento das Notícias Recentes")
st.caption("Dados capturados autonomamente do portal Agência Brasil")

path_noticias_csv = BASE_DIR / "data" / "processed" / "noticias_pcd.csv"

if path_noticias_csv.exists():
    df_noticias = pd.read_csv(path_noticias_csv)
    st.dataframe(df_noticias, use_container_width=True)

    # Processamento simples de frequência de palavras para estatísticas e nuvem de palavras
    texto_completo = " ".join(df_noticias["manchete"].dropna()).lower()
    
    # Filtro de stop words simples
    stopwords_custom = ["sobre", "para", "como", "com", "mais", "pela", "pelo", "entre", "esta", "estão", "onde", "para", "qual"]
    palavras = [p for p in texto_completo.split() if len(p) > 3 and p not in stopwords_custom]
    
    col_graph1, col_graph2 = st.columns(2)

    with col_graph1:
        st.markdown("#### 📊 Termos Mais Frequentes na Mídia")
        contagem = Counter(palavras).most_common(10)
        df_chart = pd.DataFrame(contagem, columns=["Palavra", "Frequência"]).set_index("Palavra")
        st.bar_chart(df_chart)

    with col_graph2:
        st.markdown("#### ☁️ Nuvem de Palavras das Notícias")
        if texto_completo.strip():
            wordcloud = WordCloud(width=600, height=350, background_color="white").generate(texto_completo)
            fig, ax = plt.subplots(figsize=(6, 3.5))
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)
else:
    st.info("💡 Nenhuma notícia encontrada na pasta `data/processed/`. Execute o script `python src/coleta_web.py` no seu terminal para extrair as notícias.")

st.divider()

# Serviço de upload de arquivos
st.markdown("### 📥 Serviço de Upload e Ingestão de Dados Internos")

arquivo_upload = st.file_uploader("Selecione um arquivo CSV com novos dados:", type=["csv"])

if arquivo_upload is not None:
    try:
        df_uploaded = pd.read_csv(arquivo_upload)
        st.success("Arquivo carregado com sucesso!")
        st.dataframe(df_uploaded.head(5), use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao processar o arquivo enviado: {e}")

st.divider()

# Fontes de inspiração e ecossistema
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
st.caption("IncluaTech • Projeto Prático TP2 • Ciência de Dados • 2026")