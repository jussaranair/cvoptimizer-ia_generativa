
import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

GROQ_API_URL = os.getenv("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLAMA3_MODEL = "llama3-70b-8192"


# Função utilitária para carregar prompts do arquivo system_prompt.txt
def _load_prompt(prompt_key: str) -> str:
	prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "system_prompt.txt")
	with open(prompt_path, "r", encoding="utf-8") as f:
		lines = f.readlines()
	prompt = []
	found = False
	for line in lines:
		if line.strip().startswith(f"{prompt_key}:"):
			found = True
			continue
		if found:
			if line.strip().startswith("#") or line.strip().endswith(":"):
				break
			prompt.append(line)
	return "".join(prompt).strip()

def analyze_resume_llm(resume_text: str, temperature: float = 0.2, max_tokens: int = 1024) -> Optional[Dict]:
	"""
	Envia o texto do currículo para o LLM (Llama 3-70B via Groq) e retorna o resultado estruturado.
	O prompt é carregado automaticamente do arquivo system_prompt.txt.
	"""
	prompt_template = _load_prompt("ANALYZE_RESUME_PROMPT")
	if not GROQ_API_KEY:
		raise RuntimeError("GROQ_API_KEY não definido no .env")
	headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
	data = {
		"model": LLAMA3_MODEL,
		"messages": [
			{"role": "system", "content": prompt_template},
			{"role": "user", "content": resume_text}
		],
		"temperature": temperature,
		"max_tokens": max_tokens
	}
	response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=30)
	response.raise_for_status()
	content = response.json()["choices"][0]["message"]["content"]
	try:
		import json
		return json.loads(content)
	except Exception:
		return {"raw": content}

def generate_missing_keywords_llm(resume_text: str, temperature: float = 0.2, max_tokens: int = 256) -> Optional[List[str]]:
	"""
	Envia o texto do currículo para o LLM e retorna apenas a lista de palavras-chave faltantes.
	O prompt é carregado automaticamente do arquivo system_prompt.txt.
	"""
	prompt_template = _load_prompt("MISSING_KEYWORDS_PROMPT")
	if not GROQ_API_KEY:
		raise RuntimeError("GROQ_API_KEY não definido no .env")
	headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
	data = {
		"model": LLAMA3_MODEL,
		"messages": [
			{"role": "system", "content": prompt_template},
			{"role": "user", "content": resume_text}
		],
		"temperature": temperature,
		"max_tokens": max_tokens
	}
	response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=30)
	response.raise_for_status()
	content = response.json()["choices"][0]["message"]["content"]
	try:
		import json
		return json.loads(content)
	except Exception:
		return [content]
