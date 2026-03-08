import os
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "hf")
HF_TOKEN = os.getenv("HF_TOKEN", os.getenv("HF_API_KEY", ""))
OPENAI_BASE_URL = os.getenv(
	"OPENAI_BASE_URL",
	"https://router.huggingface.co/v1"
)
OALD_API = os.getenv("OALD_API_URL", "http://127.0.0.1:8001/api/parse")
MODEL = os.getenv("LLM_MODEL", "openai/gpt-oss-20b:groq")
FALLBACK_MODELS = [
	m.strip() for m in os.getenv(
		"FALLBACK_MODELS",
		"meta-llama/Llama-3.1-8B-Instruct:cerebras"
	).split(",") if m.strip()
]
TIMEOUT = int(os.getenv("LLM_TIMEOUT", "60"))