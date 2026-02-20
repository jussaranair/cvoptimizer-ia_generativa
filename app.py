import streamlit as st
import os
from pathlib import Path
from src import cv_database

st.set_page_config(page_title="CV Optimizer - Upload Currículo", page_icon="📄")
#st.title("CV Optimizer")
#st.header("Enviar Currículo")

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

st.set_page_config(page_title="CV Optimizer - Upload Currículo", page_icon="📄")
st.markdown("""
<div class='card'>
    <div class='card-title'>CV Optimizer</div>
    <div class='card-section-title'>Enviar Currículo</div>
""", unsafe_allow_html=True)

with st.form("upload_form", clear_on_submit=True):
    name = st.text_input("Nome completo", max_chars=100)
    email = st.text_input("E-mail", max_chars=100)
    uploaded_file = st.file_uploader("Currículo (PDF ou DOCX)", type=["pdf", "docx"], accept_multiple_files=False)
    submit = st.form_submit_button("Enviar")

if submit:
    if not name or not email or not uploaded_file:
        st.error("Por favor, preencha todos os campos e envie um arquivo.")
    else:
        uploads_dir = Path("uploads")
        uploads_dir.mkdir(exist_ok=True)
        file_path = uploads_dir / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        cv_database.create_tables()  # Garante que as tabelas existem
        resume_id = cv_database.insert_resume(name, email, str(file_path))
        st.success(f"Currículo enviado com sucesso! ID: {resume_id}")
        st.info(f"Arquivo salvo em: {file_path}")

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div style='margin-top:2rem; text-align:center; color:#000000;'>CV Optimizer &copy; 2026</div>", unsafe_allow_html=True)
