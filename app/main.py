from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from pathlib import Path
import os

from app.routes import trial
from app.routes import home

# cd .. and then export PYTHONPATH=$(pwd)

app = FastAPI()

# TODO: just question, without this line it still works, what is this for?
# Get the absolute path to the app directory
BASE_DIR = Path(__file__).resolve().parent

# Mount static files using absolute path
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Middleware (optional CORS), for frontend
# TODO: in case there's react or other front end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://spaeholderforfuturefrontendnotexistedyethaha.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(home.router)
app.include_router(trial.router)