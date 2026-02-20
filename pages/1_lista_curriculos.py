import streamlit as st
from src import cv_database

st.set_page_config(page_title="Lista de Currículos", page_icon="📋")
st.title("Currículos Enviados")

resumes = cv_database.get_all_resumes()

if not resumes:
    st.info("Nenhum currículo enviado ainda.")
else:
    st.write("## Currículos")
    for resume in resumes:
        cols = st.columns([3, 4, 3, 2])
        cols[0].write(resume["name"])
        cols[1].write(resume["email"])
        cols[2].write(resume["upload_date"])
        view_btn = cols[3].button("Ver Análise", key=f"view_{resume['id']}")
        if view_btn:
            st.info(f"(Mock) Análise para {resume['name']} (ID: {resume['id']})")
    # Cabeçalho da tabela
    st.markdown("""
    <style>
    .stColumns > div:first-child { font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)
    st.write("")
    # Tabela cabeçalho manual
    st.columns([3, 4, 3, 2])[0].write("**Nome**")
    st.columns([3, 4, 3, 2])[1].write("**E-mail**")
    st.columns([3, 4, 3, 2])[2].write("**Data de Envio**")
    st.columns([3, 4, 3, 2])[3].write("")
