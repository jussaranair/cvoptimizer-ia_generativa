import streamlit as st
from src import cv_database
from mock_analysis import generate_mock_analysis
import pandas as pd

st.set_page_config(page_title="Comparar Currículos", page_icon="⚖️")
#st.title("Comparar Análises de Currículos")

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

st.set_page_config(page_title="Comparar Currículos", page_icon="⚖️")

st.markdown("""
<div class='card'>
    <div class='card-title'>Comparar Análises de Currículos</div>
""", unsafe_allow_html=True)


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

            st.markdown("<div class='card-section-title' style='margin-top:1rem;'>Pontuações por Seção</div>", unsafe_allow_html=True)
            score_labels = ["Resumo", "Experiência", "Habilidades", "Educação"]
            keys = ["summary_score", "experience_score", "skills_score", "education_score"]
            # Métricas lado a lado
            for i, label in enumerate(score_labels):
                cols = st.columns(2)
                v1 = a1[keys[i]]
                v2 = a2[keys[i]]
                delta = v2 - v1
                cols[0].metric(f"{label} (1)", v1)
                cols[1].metric(f"{label} (2)", v2, delta=delta)

            with st.expander("Detalhes das Análises e Palavras-chave Faltantes"):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"<div style='font-weight:600; color:#2563EB;'>Palavras-chave faltantes ({r1['name']}):</div>", unsafe_allow_html=True)
                    st.write(", ".join(a1["keywords_missing"]))
                with c2:
                    st.markdown(f"<div style='font-weight:600; color:#2563EB;'>Palavras-chave faltantes ({r2['name']}):</div>", unsafe_allow_html=True)
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

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div style='margin-top:2rem; text-align:center; color:#000000;'>CV Optimizer &copy; 2026</div>", unsafe_allow_html=True)
