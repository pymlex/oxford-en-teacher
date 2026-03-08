from fake_useragent import UserAgent
import requests
import re

ua = UserAgent()

def get_wiktionary_etymology(word, lang="English"):
    url = "https://en.wiktionary.org/w/api.php"
    headers = {"User-Agent": ua.random}
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": word,
        "rvprop": "content",
        "rvslots": "main"
    }
    r = requests.get(url, params=params, headers=headers, timeout=10)
    data = r.json()
    pages = data["query"]["pages"]
    page = next(iter(pages.values()))
    revisions = page.get('revisions', None)
    if revisions is None:
        return None
    text = page["revisions"][0]["slots"]["main"]["*"]
    lang_section = re.search(rf"==\s*{re.escape(lang)}\s*==(.+?)(\n==[^=]|$)", text, re.S)
    if not lang_section:
        return None
    lang_text = lang_section.group(1)
    etymology = re.search(r"===\s*Etymology.*?===(.*?)(\n===|\Z)", lang_text, re.S)
    if etymology:
        return etymology.group(1).strip()
    return None