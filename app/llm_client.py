import os
import json
import requests
from typing import Optional
from openai import OpenAI
from .config import (
	PROVIDER, OPENAI_KEY, HF_API_KEY,
	MODEL, FALLBACK_MODELS, TIMEOUT
)

class LLMClient:
	def __init__(self):
		self.provider = PROVIDER
		self.openai_client = None
		if OPENAI_KEY:
			self.openai_client = OpenAI(api_key=OPENAI_KEY)
		self.hf_key = HF_API_KEY

	def _call_openai(self, prompt: str, model: str) -> Optional[str]:
		if not self.openai_client:
			return None
		resp = self.openai_client.chat.completions.create(
			model=model,
			messages=[{"role": "user", "content": prompt}],
			temperature=0.0
		)
		choices = getattr(resp, "choices", None) or resp.get("choices", [])
		if not choices:
			return None
		first = choices[0]
		msg = first.get("message") if isinstance(first, dict) else getattr(first, "message", None)
		if not msg:
			return None
		if isinstance(msg, dict):
			return msg.get("content", "")
		return getattr(msg, "content", "")

	def _call_hf(self, prompt: str, model: str) -> Optional[str]:
		key = self.hf_key
		if not key:
			return None
		url = f"https://api-inference.huggingface.co/models/{model}"
		headers = {"Authorization": f"Bearer {key}"}
		payload = {"inputs": prompt, "options": {"wait_for_model": True}}
		try:
			r = requests.post(
				url,
				headers=headers,
				json=payload,
				timeout=TIMEOUT
			)
			if r.status_code != 200:
				return None
			j = r.json()
			if isinstance(j, list):
				text = j[0].get("generated_text") if j and isinstance(j[0], dict) else None
				if text:
					return text
			if isinstance(j, dict):
				if "generated_text" in j:
					return j["generated_text"]
				if "error" in j:
					return None
				out = j.get("generated_text") or j.get("outputs") or j.get("text")
				if out:
					return out
			return None
		except Exception:
			return None

	def generate(self, prompt: str) -> str:
		if self.provider in ("openai", "openai-first"):
			out = self._call_openai(prompt, MODEL)
			if out:
				return out
			for fb in FALLBACK_MODELS:
				out = self._call_openai(prompt, fb)
				if out:
					return out
		if self.provider in ("hf", "huggingface"):
			out = self._call_hf(prompt, MODEL)
			if out:
				return out
			for fb in FALLBACK_MODELS:
				out = self._call_hf(prompt, fb)
				if out:
					return out
		out = None
		if self.openai_client:
			out = self._call_openai(prompt, MODEL)
		if out:
			return out
		return "LLM error: no provider available or all calls failed."

client = LLMClient()