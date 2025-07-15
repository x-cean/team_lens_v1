from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import os

from routes import home


app = FastAPI()

# TODO: just question, without this line it still works, what is this for?
# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

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