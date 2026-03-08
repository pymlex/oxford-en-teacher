from uvicorn import run
from app.server import app
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
	run(
		"app.server:app",
		host="0.0.0.0",
		port=8002,
		reload=True
	)