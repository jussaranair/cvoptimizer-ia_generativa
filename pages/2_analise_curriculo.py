
import streamlit as st
from src import cv_database
from mock_analysis import generate_mock_analysis
import pandas as pd
from pathlib import Path

# Verifica existência do banco de dados
db_path = Path(__file__).resolve().parent.parent.parent / "cvoptimizer.db"
if not db_path.exists():
    st.warning("O banco de dados ainda não foi criado. Envie pelo menos um currículo para inicializar o sistema.")
    st.stop()

st.set_page_config(page_title="Análise de Currículo", page_icon="📊")
#st.title("Análise de Currículo")

# --- Custom CSS for Light Premium Dashboard ---
st.markdown("""
<style>
body, .stApp {
    background: #F8FAFC !important;
}
header, .st-emotion-cache-18ni7ap, .st-emotion-cache-6qob1r {
    display: none !important;
}
.stSidebar, section[data-testid="stSidebar"], .css-1d391kg, .st-emotion-cache-1d391kg {
    background: #FFFFFF !important;
    color: #000000 !important;
    border-right: 1.5px solid #E2E8F0 !important;
}
.stMarkdown, .stHeader, .stTitle, h1, h2, h3, h4, h5, h6, label, .stTextInput>div>div>input, .stTextInput>div>div>div>input, .stTextInput label, .stTextInput, .stTextInput>div>div>input::placeholder {
    color: #000000 !important;
}
.stTextInput>div>div>input, .stTextInput>div>div>div>input {
    background: #FFFFFF !important;
    border: 1.5px solid #E2E8F0 !important;
    color: #000000 !important;
}
.stButton>button {
    background: #2563EB !important;
    color: #FFFFFF !important;
    border-radius: 12px;
    font-weight: 700;
    border: none;
    padding: 0.6rem 1.7rem;
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
    transition: background 0.2s;
    font-size: 1.08rem;
}
.stButton>button:hover {
    background: #0EA5E9 !important;
    color: #FFFFFF !important;
}
.stExpander {
    background: #FFFFFF !important;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
    margin-bottom: 1.2rem;
    color: #000000 !important;
    border: 1.5px solid #E2E8F0 !important;
}
.stMetric {
    background: #FFFFFF !important;
    border-radius: 12px;
    padding: 1.1rem;
    margin-bottom: 1.1rem;
    color: #000000 !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
    border: 1.5px solid #E2E8F0 !important;
}
.stAlert, .stSuccess, .stInfo, .stError {
    background: #FFFFFF !important;
    color: #000000 !important;
    border-left: 5px solid #2563EB !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
}
.stFileUploader, .stFileUploader label {
    color: #000000 !important;
}
.stFileUploader>div>div {
    background: #FFFFFF !important;
    border: 1.5px solid #E2E8F0 !important;
}
.st-cq, .st-cp, .st-cq .st-cp {
    color: #000000 !important;
}
.stDataFrame, .stDataFrame th, .stDataFrame td {
    background: #FFFFFF !important;
    color: #000000 !important;
    border-color: #E2E8F0 !important;
}
.st-bb, .st-bc, .st-bd {
    color: #000000 !important;
}
.stCaption, .st-emotion-cache-1v0mbdj {
    color: #0EA5E9 !important;
}
.card {
    background: #FFFFFF;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
    padding: 2.2rem 2rem 1.5rem 2rem;
    margin-bottom: 2.2rem;
    border: 1.5px solid #E2E8F0;
}
.card-title {
    color: #000000;
    font-size: 2.1rem;
    font-weight: 700;
    margin-bottom: 1.2rem;
    letter-spacing: -1px;
}
.card-section-title {
    color: #2563EB;
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 0.7rem;
    margin-top: 1.2rem;
    letter-spacing: -0.5px;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Análise de Currículo", page_icon="📊")

st.markdown("""
<div class='card'>
    <div class='card-title'>Análise de Currículo</div>
""", unsafe_allow_html=True)

resumes = cv_database.get_all_resumes()


if not resumes:
    st.info("Nenhum currículo disponível para análise.")
    st.stop()
else:
    options = {f"{r['name']} ({r['email']}) [{r['upload_date']}]": r for r in resumes}
    selected = st.selectbox("Selecione um currículo para analisar:", list(options.keys()))
    resume = options[selected]

    # TODO: Substituir generate_mock_analysis() por chamada à IA generativa
    analysis = generate_mock_analysis()

    st.markdown(f"<div class='card-section-title'>Análise de: {resume['name']}</div>", unsafe_allow_html=True)

    # TODO: Substituir métricas por dados vindos da IA generativa
    cols = st.columns(4)
    cols[0].metric("Resumo", analysis["summary_score"])
    cols[1].metric("Experiência", analysis["experience_score"])
    cols[2].metric("Habilidades", analysis["skills_score"])
    cols[3].metric("Educação", analysis["education_score"])

    st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='card-section-title'>Pontuação por Seção</div>", unsafe_allow_html=True)

    # TODO: Substituir chart_data/bar_chart por dados vindos da IA generativa
    chart_data = pd.DataFrame({
        "Seção": ["Resumo", "Experiência", "Habilidades", "Educação"],
        "Pontuação": [
            analysis["summary_score"],
            analysis["experience_score"],
            analysis["skills_score"],
            analysis["education_score"]
        ]
    })
    st.bar_chart(chart_data.set_index("Seção"))


    # TODO: Substituir keywords_missing por lista gerada pela IA generativa
    with st.expander("Palavras-chave faltantes"):
        st.markdown("<div style='font-weight:600; color:#2563EB;'>Palavras-chave faltantes:</div>", unsafe_allow_html=True)
        st.write(", ".join(analysis["keywords_missing"]))

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div style='margin-top:2rem; text-align:center; color:#000000;'>CV Optimizer &copy; 2026</div>", unsafe_allow_html=True)
