import streamlit as st
import pandas as pd
from pathlib import Path
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.set_page_config(page_title="IncluaTech | Notícias", page_icon="📰", layout="wide")

# Identificação do projeto
with st.sidebar:
    st.title("♿ IncluaTech")
    st.caption("Painel de Governança ESG & Inclusão PcD")
    st.divider()

BASE_DIR = Path(__file__).resolve().parent.parent
path_noticias_csv = BASE_DIR / "data" / "processed" / "noticias_pcd.csv"

st.title("📰 Monitorização das Notícias Recentes")
st.caption("Dados capturados autonomamente do portal Agência Brasil")
st.divider()

if path_noticias_csv.exists():
    df_noticias = pd.read_csv(path_noticias_csv)
    st.dataframe(df_noticias, use_container_width=True)

    texto_completo = " ".join(df_noticias["manchete"].dropna()).lower()
    
    stopwords_custom = ["sobre", "para", "como", "com", "mais", "pela", "pelo", "entre", "esta", "estão", "onde", "qual"]
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
    st.info("💡 Nenhuma notícia encontrada em `data/processed/noticias_pcd.csv`. Execute o script de scraping no terminal para gerar os dados.")