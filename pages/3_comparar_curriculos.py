import streamlit as st
from src import cv_database
from mock_analysis import generate_mock_analysis
import pandas as pd

st.set_page_config(page_title="Comparar Currículos", page_icon="⚖️")
st.title("Comparar Análises de Currículos")

resumes = cv_database.get_all_resumes()

if len(resumes) < 2:
    st.info("Cadastre pelo menos dois currículos para comparar.")
else:
    options = {f"{r['name']} ({r['email']}) [{r['upload_date']}]": r for r in resumes}
    col1, col2 = st.columns(2)
    with col1:
        sel1 = st.selectbox("Currículo 1", list(options.keys()), key="sel1")
    with col2:
        sel2 = st.selectbox("Currículo 2", list(options.keys()), key="sel2")
    if sel1 == sel2:
        st.warning("Selecione dois currículos diferentes.")
    else:
        r1 = options[sel1]
        r2 = options[sel2]
        a1 = generate_mock_analysis()
        a2 = generate_mock_analysis()
        # Scores lado a lado
        st.subheader("Pontuações por Seção")
        score_labels = ["Resumo", "Experiência", "Habilidades", "Educação"]
        keys = ["summary_score", "experience_score", "skills_score", "education_score"]
        table = []
        for label, k in zip(score_labels, keys):
            v1 = a1[k]
            v2 = a2[k]
            # Cores: verde se melhorou, vermelho se piorou, cinza igual
            if v2 > v1:
                color1 = "#ffcccc"  # vermelho claro
                color2 = "#ccffcc"  # verde claro
            elif v2 < v1:
                color1 = "#ccffcc"
                color2 = "#ffcccc"
            else:
                color1 = color2 = "#f0f0f0"
            table.append((label, v1, v2, color1, color2))
        # Renderizar tabela customizada
        st.markdown("<style>th,td {text-align:center !important;}</style>", unsafe_allow_html=True)
        st.write("<table><tr><th>Seção</th><th>Currículo 1</th><th>Currículo 2</th></tr>", unsafe_allow_html=True)
        for label, v1, v2, c1, c2 in table:
            st.write(f"<tr><td>{label}</td><td style='background-color:{c1}'>{v1}</td><td style='background-color:{c2}'>{v2}</td></tr>", unsafe_allow_html=True)
        st.write("</table>", unsafe_allow_html=True)
        # Palavras-chave faltantes
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"**Palavras-chave faltantes ({r1['name']}):**")
            st.write(", ".join(a1["keywords_missing"]))
        with c2:
            st.write(f"**Palavras-chave faltantes ({r2['name']}):**")
            st.write(", ".join(a2["keywords_missing"]))
