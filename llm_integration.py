
import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

GROQ_API_URL = os.getenv("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLAMA3_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


# Função utilitária para carregar prompts do arquivo system_prompt.txt

def _load_prompt() -> str:
	prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "system_prompt.txt")
	with open(prompt_path, "r", encoding="utf-8") as f:
		return f.read().strip()

def analyze_resume_llm(resume_text: str, temperature: float = 0.2, max_tokens: int = 1024) -> Optional[Dict]:
	"""
	Envia o texto do currículo para o LLM (Llama 3-70B via Groq) e retorna o resultado estruturado.
	O prompt é carregado automaticamente do arquivo system_prompt.txt.
	"""
	prompt_template = _load_prompt()
	print("[DEBUG] GROQ_API_URL:", GROQ_API_URL)
	print("[DEBUG] GROQ_API_KEY:", GROQ_API_KEY[:6], "... (ocultado)")
	print("[DEBUG] Modelo:", LLAMA3_MODEL)
	print("[DEBUG] Prompt carregado:", repr(prompt_template[:120]))
	print("[DEBUG] Texto do currículo (primeiros 120 chars):", repr(resume_text[:120]))
	print("[DEBUG] max_tokens:", max_tokens)
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
	print("[DEBUG] Payload enviado:", data)
	try:
		response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=30)
		print("[DEBUG] Status code:", response.status_code)
		print("[DEBUG] Response text:", response.text[:500])
		response.raise_for_status()
		content = response.json()["choices"][0]["message"]["content"]
		import json, re
		# Tenta extrair JSON de qualquer parte do texto
		json_match = re.search(r'\{.*\}', content, re.DOTALL)
		if json_match:
			try:
				return json.loads(json_match.group(0))
			except Exception as e:
				print("[ERROR] Falha ao carregar JSON extraído:", e)
				return {"raw": content}
		else:
			print("[WARN] Resposta não contém JSON. Retornando texto bruto.")
			return {"raw": content}
	except Exception as e:
		print("[ERROR] Exception ao chamar Groq:", e)
		return {"error": str(e)}

