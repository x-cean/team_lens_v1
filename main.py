from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import os

from routes import home, query


# TODO: pipeline is basically like this, need to think about
# todo: 1 data structure: database not only general login and others but also file vector storage,
#  chat history storage, etc. In the trial page now, the file uploaded is not stored, maybe it should be.
#  Did i get it right that chatting to germini via api once also has memory in that one chat?
# todo: 2 better embedding and similarity logic? better ready to be used tools?
# todo: 3 backend structure, plan the endpoints
# todo: 4 look for further useful info


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