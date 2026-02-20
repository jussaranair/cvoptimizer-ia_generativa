import streamlit as st
import os
from pathlib import Path
from src import cv_database

st.set_page_config(page_title="CV Optimizer - Upload Currículo", page_icon="📄")
st.title("CV Optimizer")
st.header("Enviar Currículo")

# Formulário de upload e dados básicos
with st.form("upload_form", clear_on_submit=True):
    name = st.text_input("Nome completo", max_chars=100)
    email = st.text_input("E-mail", max_chars=100)
    uploaded_file = st.file_uploader("Currículo (PDF ou DOCX)", type=["pdf", "docx"], accept_multiple_files=False)
    submit = st.form_submit_button("Enviar")

if submit:
    if not name or not email or not uploaded_file:
        st.error("Por favor, preencha todos os campos e envie um arquivo.")
    else:
        # Salvar arquivo
        uploads_dir = Path("uploads")
        uploads_dir.mkdir(exist_ok=True)
        file_path = uploads_dir / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        # Salvar info no banco
        cv_database.create_tables()  # Garante que as tabelas existem
        resume_id = cv_database.insert_resume(name, email, str(file_path))
        st.success(f"Currículo enviado com sucesso! ID: {resume_id}")
        st.info(f"Arquivo salvo em: {file_path}")
