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
    tab1, tab2 = st.tabs(["Selecionar Currículos", "Comparação Visual"])

    with tab1:
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

            st.subheader("Pontuações por Seção")
            score_labels = ["Resumo", "Experiência", "Habilidades", "Educação"]
            keys = ["summary_score", "experience_score", "skills_score", "education_score"]
            # Métricas lado a lado
            for i, label in enumerate(score_labels):
                cols = st.columns(2)
                v1 = a1[keys[i]]
                v2 = a2[keys[i]]
                delta = v2 - v1
                color = "normal"
                if delta > 0:
                    color = "inverse"  # verde
                elif delta < 0:
                    color = "off"  # vermelho
                cols[0].metric(f"{label} (1)", v1)
                cols[1].metric(f"{label} (2)", v2, delta=delta)

            # Expander para detalhes
            with st.expander("Detalhes das Análises e Palavras-chave Faltantes"):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**Palavras-chave faltantes ({r1['name']}):**")
                    st.write(", ".join(a1["keywords_missing"]))
                with c2:
                    st.write(f"**Palavras-chave faltantes ({r2['name']}):**")
                    st.write(", ".join(a2["keywords_missing"]))

    with tab2:
        # Gráfico de barras comparativo
        if 'sel1' in locals() and 'sel2' in locals() and sel1 != sel2:
            r1 = options[sel1]
            r2 = options[sel2]
            a1 = generate_mock_analysis()
            a2 = generate_mock_analysis()
            chart_data = {
                'Seção': score_labels,
                f'{r1["name"]}': [a1[k] for k in keys],
                f'{r2["name"]}': [a2[k] for k in keys],
            }
            df = pd.DataFrame(chart_data).set_index('Seção')
            st.bar_chart(df)
            st.write("As barras mostram a pontuação de cada seção para ambos os currículos.")
