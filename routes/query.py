from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os
from pydantic import BaseModel


templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "templates"))
router = APIRouter()


@router.get("/trial", response_class=HTMLResponse)
def trial_page(request: Request):
    return templates.TemplateResponse("trial.html", {"request": request})


@router.post("/trial", response_class=HTMLResponse)
def trial_post(request: Request):
    pass


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    return {"filename": file.filename, "size": len(content)}

# using pydantic to validate msg datatype
class ChatMessage(BaseModel):
    message: str

@router.post("/chat")
async def chat(message: ChatMessage):
    reply = f"Echo: {message.message}"
    return JSONResponse(content={"reply": reply})