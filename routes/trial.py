from fastapi import APIRouter, Request, UploadFile, File, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
import io
import os

from team_lens_v1.datamanager.models import TrialMessage
from team_lens_v1.services.rag.parser import extract_text_from_pdf_like_object
from team_lens_v1.services.rag.simple_rag_pipeline_spacy_embedding_sklearn_similarity_germini \
    import simple_rag_pipeline

from team_lens_v1.datamanager.sql_postgre_datamanager import PostgresDataManager


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
    question: str = Form(...),
    chat_id: int | None = Form(None),
    session: Session = Depends(PostgresDataManager.postgresql_init)
):
    content = await file.read() if file else None
    # get str from pdf-like object
    doc = extract_text_from_pdf_like_object(io.BytesIO(content)) if content else ""
    # call the function
    answer = simple_rag_pipeline(doc, question)

    #todo: save chat history to a database, here need to figure more about dependencies and how to sep users
    data_manager = PostgresDataManager(session=session)
    if chat_id is None:
        a_trial_chat = data_manager.create_trial_chat()
        chat_id = a_trial_chat.id
    # Save the user message
    a_question_message = TrialMessage(
        chat_id=chat_id,
        text=question
    )
    an_answer_message = TrialMessage(
        chat_id=chat_id,
        text=answer,
        is_system=True,
        is_user=False
    )
    data_manager.save_trial_message(a_question_message)
    data_manager.save_trial_message(an_answer_message)

    return JSONResponse({"answer": answer, "chat_id": chat_id})



    return JSONResponse({"answer": answer})
