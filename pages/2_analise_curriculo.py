import streamlit as st
from src import cv_database
from mock_analysis import generate_mock_analysis
import pandas as pd

st.set_page_config(page_title="Análise de Currículo", page_icon="📊")
st.title("Análise de Currículo")

resumes = cv_database.get_all_resumes()

if not resumes:
    st.info("Nenhum currículo disponível para análise.")
else:
    options = {f"{r['name']} ({r['email']}) [{r['upload_date']}]": r for r in resumes}
    selected = st.selectbox("Selecione um currículo para analisar:", list(options.keys()))
    resume = options[selected]
    analysis = generate_mock_analysis()

    st.subheader(f"Análise de: {resume['name']}")
    # Métricas em colunas
    cols = st.columns(4)
    cols[0].metric("Resumo", analysis["summary_score"])
    cols[1].metric("Experiência", analysis["experience_score"])
    cols[2].metric("Habilidades", analysis["skills_score"])
    cols[3].metric("Educação", analysis["education_score"])

    # Gráfico de barras
    st.write("")
    st.write("### Pontuação por Seção")
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

    # Palavras-chave faltantes
    with st.expander("Palavras-chave faltantes"):
        st.write(", ".join(analysis["keywords_missing"]))
