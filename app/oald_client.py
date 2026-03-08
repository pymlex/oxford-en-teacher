import requests
from app.config import OALD_API
from dotenv import load_dotenv
load_dotenv()

def query_oald(word):
	r = requests.get(OALD_API, params={"word": word}, timeout=8)
	return r.json()