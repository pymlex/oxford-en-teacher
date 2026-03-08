from pathlib import Path

PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "llm_prompt.md"

def load_template():
    text = PROMPT_PATH.read_text(encoding="utf-8")
    return text

def build_prompt(user_text, oald_entries, wiktionary_entries=None):
    tpl = load_template()
    context = ""
    for e in oald_entries:
        context += f"\n\n---\nOALD {e.get('word')} (page {e.get('page_index')})\n"
        if e.get("part_of_speech"):
            context += f"- POS: {e.get('part_of_speech')}\n"
        phon = e.get("phonetics", {})
        if phon:
            context += f"- phonetics: uk {phon.get('uk')} | us {phon.get('us')}\n"
        for s in e.get("senses", []):
            context += f"- def: {s.get('definition')}\n"
            for ex in s.get("examples", []):
                context += f"  - ex: {ex}\n"
        if e.get("origin"):
            context += f"- origin: {e.get('origin')}\n"
    wik = ""
    if wiktionary_entries:
        for w, origin in wiktionary_entries.items():
            if origin:
                wik += f"\n\n---\nWIKTIONARY {w}\n- origin: {origin}\n"
    prompt = tpl.replace("{user_text}", user_text).replace(
        "{oald_entries}", context
    ).replace("{wiktionary_entries}", wik)
    return prompt