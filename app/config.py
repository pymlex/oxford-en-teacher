import os

PROVIDER = os.getenv("LLM_PROVIDER", "hf")
HF_API_KEY = os.getenv("HF_API_KEY", "token is missing, set it in .env")
MODEL = os.getenv("LLM_MODEL", "openai/gpt-oss-20b:groq")
FALLBACK_MODELS = os.getenv(
	"FALLBACK_MODELS",
	"meta-llama/Llama-3.1-8B-Instruct:cerebras"
).split(",")
TIMEOUT = int(os.getenv("LLM_TIMEOUT", "60"))