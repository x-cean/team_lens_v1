from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import io
import os
from pydantic import BaseModel

from team_lens_v1.services.rag.parser import extract_text_from_pdf_like_object
from team_lens_v1.services.rag.simple_rag_pipeline_spacy_embedding_sklearn_similarity_germini \
    import simple_rag_pipeline


templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "templates"))
router = APIRouter()


@router.get("/trial", response_class=HTMLResponse)
def trial_page(request: Request):
    return templates.TemplateResponse("trial.html", {"request": request})


@router.post("/trial", response_class=HTMLResponse)
def trial_post(request: Request):
    pass


@router.post("/ask")
async def ask(
    file: UploadFile | None = File(None),
    question: str = Form(...)
):
    content = await file.read() if file else None
    # get str from pdf-like object
    doc = extract_text_from_pdf_like_object(io.BytesIO(content)) if content else ""
    # call the function
    answer = simple_rag_pipeline(doc, question)
    return JSONResponse({"answer": answer})
