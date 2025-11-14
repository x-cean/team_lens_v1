from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import os

from team_lens_v1.app.routes import trial
from team_lens_v1.app.routes import home

# cd .. and then export PYTHONPATH=$(pwd)

app = FastAPI()

# TODO: just question, without this line it still works, what is this for?
# Mount static files
app.mount("/static", StaticFiles(
    directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

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