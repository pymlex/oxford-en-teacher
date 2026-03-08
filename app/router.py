from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from app.oald_client import query_oald
from app.prompt_builder import build_prompt
from app.llm_client import client
from app.wiktionary_client import get_wiktionary_etymology

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
    unique_words = []
    for t in tokens:
        tw = t.strip().lower()
        if tw and tw.isalpha() and tw not in unique_words:
            unique_words.append(tw)
    wik = {}
    for w in unique_words:
        origin = get_wiktionary_etymology(w)
        if origin:
            wik[w] = origin
    prompt = build_prompt(text, entries, wik)
    res_text = client.generate(prompt)
    return {"status": "ok", "answer_md": res_text}
    
@router.post("/stop")
def stop(background_tasks: BackgroundTasks):
    background_tasks.add_task(__import__("os")._exit, 0)
    return {"status": "stopping"}