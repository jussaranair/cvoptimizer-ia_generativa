import streamlit as st
from src import cv_database
from mock_analysis import generate_mock_analysis
import pandas as pd

st.set_page_config(page_title="CV Optimizer", page_icon="📋")

st.header("Currículos Enviados")
resumes = cv_database.get_all_resumes()

if not resumes:
    st.info("Nenhum currículo enviado ainda.")
else:
    # Table header
    header_cols = st.columns([3, 4, 3, 2])
    header_cols[0].markdown("**Nome**")
    header_cols[1].markdown("**E-mail**")
    header_cols[2].markdown("**Data de Envio**")
    header_cols[3].markdown("")

    # Table rows
    for resume in resumes:
        row_cols = st.columns([3, 4, 3, 2])
        row_cols[0].write(resume["name"])
        row_cols[1].write(resume["email"])
        row_cols[2].write(resume["upload_date"])
        view_btn = row_cols[3].button("Ver Análise", key=f"view_{resume['id']}")

        if view_btn:
            with st.expander(f"Análise de {resume['name']} ({resume['email']})", expanded=True):
                analysis = generate_mock_analysis()
                # Metrics in columns
                mcols = st.columns(4)
                mcols[0].metric("Resumo", analysis["summary_score"])
                mcols[1].metric("Experiência", analysis["experience_score"])
                mcols[2].metric("Habilidades", analysis["skills_score"])
                mcols[3].metric("Educação", analysis["education_score"])
                # Bar chart for scores
                chart_data = pd.DataFrame({
                    "Seção": ["Resumo", "Experiência", "Habilidades", "Educação"],
                    "Pontuação": [
                        analysis["summary_score"],
                        analysis["experience_score"],
                        analysis["skills_score"],
                        analysis["education_score"],
                    ],
                })
                st.bar_chart(chart_data.set_index("Seção"))
                # Missing keywords
                st.markdown("**Palavras-chave faltantes:**")
                st.write(", ".join(analysis["keywords_missing"]))
