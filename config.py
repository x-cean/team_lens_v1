from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPEN_API_KEY")
GERMINI_API_KEY = os.getenv("GERMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
