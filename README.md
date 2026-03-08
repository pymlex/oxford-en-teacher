# Oxford EN Teacher

A FastAPI-based orchestrator that queries a local OALD parser, Wiktionary, and a gpt-oss-120b model via Hugging Face to return bilingual explanations, examples, phonetics, and word origins to help Russian speakers learn English precisely.

<img width="673" height="270" alt="image" src="https://github.com/user-attachments/assets/7f765dbd-6c0f-433b-95ce-e1810c959d8f" />

## Functional abilities

* Accepts free-text queries in a simple [chat](https://github.com/pymlex/unichat-gui).
* Checks pronunciations and multiple meanings in [OALD](https://www.oxfordlearnersdictionaries.com).
* Fetches [Wiktionary](https://en.wiktionary.org/wiki/api) etymology and inserts it into the prompt.
* OALD and Wiktionary requests are performed in parallel.
* Pluggable gpt-oss-120b LLM backend via [Hugging Face](https://huggingface.co/docs/inference-providers/index) client. Supports fallback models.
* Works locally (Windows) and supports Docker.

## Repo base structure

```
.
├── app/
│   ├── main.py          
│   ├── server.py        
│   ├── router.py         
│   ├── llm_client.py    
│   ├── oald_client.py    
...
│   └── config.py
├── prompts/llm_prompt.md
├── build.bat     
├── requirements.txt
└── .env
```

---

## Installation

For Windows users:

```powershell
git clone https://github.com/pymlex/oxford-en-teacher.git
cd oxford-en-teacher
.\build.bat
````

Set environment variables or create a `.env` in the repository root:

```
LLM_PROVIDER=hf
HF_API_KEY=hf_xxx...            
LLM_MODEL=openai/gpt-oss-20b:groq
FALLBACK_MODELS=meta-llama/Llama-3.1-8B-Instruct:cerebras
OPENAI_BASE_URL=[https://router.huggingface.co/v1](https://router.huggingface.co/v1)   # optional
OALD_API_URL=[http://127.0.0.1:8001/api/parse](http://127.0.0.1:8001/api/parse)       # local parser
LLM_TIMEOUT=60
```

Find your Hugging Face API key [here](https://huggingface.co/settings/tokens). The StartChat.lnk file will be automatically generated. Click it and open the http://127.0.0.1:8003/ page in your browser.

---

## Docker

A `Dockerfile` is also provided. Build and run:

```bash
docker build -t oxford-en-teacher .
docker run -e HF_API_KEY=hf_xxx -p 8002:8002 oxford-en-teacher
```

## KPI

The p95 time for an arbitrary response from the chatbot is 10 seconds. Complex queries containing multiple English words may take longer.
