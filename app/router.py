from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from app.oald_client import query_oald
from app.prompt_builder import build_prompt
from app.llm_client import client
from app.wiktionary_client import get_wiktionary_etymology
import threading
import re

router = APIRouter()

class Q(BaseModel):
    query: str

def _fetch_oald(word: str, entries: list, lock: threading.Lock):
    res = query_oald(word)
    if res and res.get("results"):
        with lock:
            entries.extend(res.get("results"))

def _fetch_wiktionary(word: str, wik: dict, lock: threading.Lock):
    origin = get_wiktionary_etymology(word)
    if origin:
        with lock:
            wik[word] = origin

@router.post("/ask")
def ask(body: Q):
    text = body.query or ""
    latin_tokens = re.findall(r"[A-Za-z]+(?:-[A-Za-z]+)*", text)
    unique_words = []
    for t in latin_tokens:
        tw = t.strip().lower()
        if tw and tw not in unique_words:
            unique_words.append(tw)

    entries = []
    entries_lock = threading.Lock()
    wik = {}
    wik_lock = threading.Lock()
    threads = []

    for w in unique_words:
        t_oald = threading.Thread(target=_fetch_oald, args=(w, entries, entries_lock))
        t_wik = threading.Thread(target=_fetch_wiktionary, args=(w, wik, wik_lock))
        t_oald.start()
        t_wik.start()
        threads.append(t_oald)
        threads.append(t_wik)

    for t in threads:
        t.join()

    prompt = build_prompt(text, entries, wik)
    res_text = client.generate(prompt)
    return {"status": "ok", "answer_md": res_text}

@router.post("/stop")
def stop(background_tasks: BackgroundTasks):
    background_tasks.add_task(__import__("os")._exit, 0)
    return {"status": "stopping"}