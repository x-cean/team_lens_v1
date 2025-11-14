from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GERMINI_API_KEY = os.getenv("GERMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_URL_2 = os.getenv("SUPABASE_URL_2")
SUPABASE_DB_STRING = os.getenv("SUPABASE_DB_STRING")
SUPABASE_DB_PASSWORD = os.getenv("SUPABASE_DB_PASSWORD")
CHROMA_API_KEY = os.getenv("CHROMA_CLOUD_API_KEY")
CHROMA_TENANT_ID = os.getenv("CHROMA_CLOUD_TENANT_ID")

# ---------- Project Paths (centralized) ----------
# Project root: package root (team_lens_v1)
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent

# Data storage directories
DATA_STORAGE_DIR: Path = PROJECT_ROOT / "data_storage"
LOGS_DIR: Path = DATA_STORAGE_DIR / "logs"

# SQLite locations
SQLITE_DB_DIR: Path = DATA_STORAGE_DIR / "sql_db"
SQLITE_DB_FILE: Path = SQLITE_DB_DIR / "team_lens.db"
SQLITE_URL: str = f"sqlite:///{SQLITE_DB_FILE}"

# Chroma persistent database directory
CHROMA_PERSISTENT_DIR: Path = DATA_STORAGE_DIR / "chroma_db" / "chroma_persistent"

# Logging files
PROJECT_LOG_FILE: Path = LOGS_DIR / "project.log"
LLM_EVAL_LOG_FILE: Path = LOGS_DIR / "llm_eval_data.jsonl"

# Ensure directories exist at import time
for _dir in (DATA_STORAGE_DIR, LOGS_DIR, SQLITE_DB_DIR, CHROMA_PERSISTENT_DIR):
    _dir.mkdir(parents=True, exist_ok=True)

