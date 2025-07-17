from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import os

from routes import home, query


# TODO: pipeline is basically like this, need to think about
# 1 data structure: database not only general login and others but also file vector storage, chat history storage, etc
# 2 better embedding and similarity logic? better ready to be used tools?
# 3 backend structure, plan the endpoints
# 4 look for further useful info


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
app.include_router(query.router)