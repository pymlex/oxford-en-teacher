from fastapi import APIRouter
from pydantic import BaseModel
from app.oald_client import query_oald
from app.prompt_builder import build_prompt
from app.llm_client import client

router = APIRouter()

class Q(BaseModel):
	query: str

@router.post("/ask")
def ask(body: Q):
	text = body.query
	tokens = [t for t in text.split() if any(c.isalpha() for c in t)]
	entries = []
	for w in tokens:
		res = query_oald(w)
		if res and res.get("results"):
			entries.extend(res.get("results"))
	prompt = build_prompt(text, entries)
	res_text = client.generate(prompt)
	return {"status": "ok", "answer_md": res_text}