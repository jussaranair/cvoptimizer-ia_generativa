import os
from pathlib import Path
from typing import Optional, List
import docx2txt
import PyPDF2
from src import cv_database
from llm_integration import analyze_resume_llm


def extract_resume_text(file_path: str) -> Optional[str]:
    """
    Extrai o texto de um currículo em PDF ou DOCX.
    Retorna o texto extraído ou None se não for possível.
    """
    ext = Path(file_path).suffix.lower()
    if ext == ".pdf":
        try:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = "\n".join(page.extract_text() or "" for page in reader.pages)
            return text.strip()
        except Exception as e:
            print(f"Erro ao extrair PDF: {e}")
            return None
    elif ext == ".docx":
        try:
            text = docx2txt.process(file_path)
            return text.strip()
        except Exception as e:
            print(f"Erro ao extrair DOCX: {e}")
            return None
    else:
        print(f"Formato não suportado: {ext}")
        return None


def analyze_and_store_resume(resume_id: int) -> Optional[int]:
    """
    Extrai o texto do currículo, faz a análise via LLM e insere os dados na tabela analyses.
    Retorna o id da análise inserida ou None.
    """
    # Busca o currículo pelo id
    resumes = cv_database.get_all_resumes()
    resume = next((r for r in resumes if r["id"] == resume_id), None)
    if not resume:
        print(f"Currículo id {resume_id} não encontrado.")
        return None
    file_path = resume["file_path"]
    resume_text = extract_resume_text(file_path)
    if not resume_text:
        print("Não foi possível extrair o texto do currículo.")
        return None
    # Chama o LLM para análise
    analysis = analyze_resume_llm(resume_text)
    if not analysis or not isinstance(analysis, dict):
        print("Análise LLM falhou.")
        return None
    # Extrai campos
    summary_score = analysis.get("summary_score")
    experience_score = analysis.get("experience_score")
    skills_score = analysis.get("skills_score")
    education_score = analysis.get("education_score")
    keywords_missing = analysis.get("keywords_missing")
    # Insere na tabela analyses
    print("[DEBUG] Dados para inserir na tabela analyses:")
    print("  resume_id:", resume_id)
    print("  summary_score:", summary_score)
    print("  experience_score:", experience_score)
    print("  skills_score:", skills_score)
    print("  education_score:", education_score)
    print("  keywords_missing:", keywords_missing)
    analysis_id = cv_database.insert_analysis(
        resume_id,
        summary_score,
        experience_score,
        skills_score,
        education_score,
        keywords_missing
    )
    if analysis_id:
        print(f"[INFO] Análise inserida com sucesso! ID: {analysis_id}")
    else:
        print("[ERROR] Falha ao inserir análise no banco.")
    return analysis_id
