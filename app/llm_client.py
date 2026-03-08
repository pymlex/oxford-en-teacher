from openai import OpenAI
from .config import (
	PROVIDER, HF_TOKEN, OPENAI_BASE_URL,
	MODEL, FALLBACK_MODELS
)

class LLMClient:
	def __init__(self):
		self.provider = PROVIDER
		self.client = None
		if HF_TOKEN:
			self.client = OpenAI(
				api_key=HF_TOKEN,
				base_url=OPENAI_BASE_URL
			)

	def _call_openai(self, prompt: str, model: str):
		resp = self.client.chat.completions.create(
			model=model,
			messages=[{"role": "user", "content": prompt}],
			temperature=0.0
		)
		choice0 = resp.choices[0]
		if isinstance(choice0, dict):
			msg = choice0.get("message") or choice0.get("delta")
		else:
			msg = getattr(choice0, "message", None) or getattr(choice0, "delta", None)
		if isinstance(msg, dict):
			return msg.get("content", "")
		return getattr(msg, "content", "")

	def generate(self, prompt: str) -> str:
		if self.client is None:
			return "HF token not set. Set HF_TOKEN in .env."
		out = self._call_openai(prompt, MODEL)
		if out:
			return out
		for fb in FALLBACK_MODELS:
			out = self._call_openai(prompt, fb)
			if out:
				return out
		return "LLM error: all calls failed."

client = LLMClient()