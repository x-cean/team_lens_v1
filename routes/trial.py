from fastapi import APIRouter, Request, UploadFile, File, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
import os

from team_lens_v1.services.rag.workflow_1_rag import rag_workflow_1
from team_lens_v1.services.llm.prompt_settings import SYSTEM_PROMPT_TRIAL

from team_lens_v1.datamanager.models import TrialMessage
from team_lens_v1.datamanager.sql_postgre_datamanager import PostgresDataManager
from team_lens_v1.datamanager.sql_database_init import fastapi_postgresql_init


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
    session: Session = Depends(fastapi_postgresql_init)
):
    content = await file.read() if file else None
    ### todo: handle the upload, or maybe input website directly and so on
    # for pdf:
    # write a file temporarily to disk if file is provided
    if content is not None:
        with open ("data/test_examples/temp_file.pdf", "wb") as f:
            if content:
                f.write(content)
    # call the function
    answer = rag_workflow_1(user_query=question,
                            pdf_path="data/test_examples/temp_file.pdf" if content else None,
                            threshold=0.4, top_k=3)

    #todo: save chat history to a database, currently chatid is always the same???
    data_manager = PostgresDataManager(session=session)
    if chat_id is None:
        a_trial_chat = data_manager.create_trial_chat()
        chat_id = a_trial_chat.id
    # save the user message
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


@router.post("/ask/{chat_id: int}")
async def ask(
    file: UploadFile | None = File(None),
    question: str = Form(...),
    session: Session = Depends(fastapi_postgresql_init)
):
    content = await file.read() if file else None
    ### todo: handle the upload, or maybe input website directly and so on
    # for pdf:
    # write a file temporarily to disk if file is provided
    if content is not None:
        with open ("data/test_examples/temp_file.pdf", "wb") as f:
            if content:
                f.write(content)
    # get the latest 10 messages from the chat history and format them with system prompt
    data_manager = PostgresDataManager(session=session)
    chat_history = data_manager.get_trial_chat_history_by_id(chat_id)
    chat_history_system = [{"role": "system", "content": SYSTEM_PROMPT_TRIAL}]
    chat_history_formatted = [{"role": "user" if msg.is_user else "assistant",
                               "content": msg.text} for msg in chat_history] if chat_history else None
    messages = chat_history_system + chat_history_formatted if chat_history_formatted else None

    # call the function
    answer = rag_workflow_1(user_query=question,
                            pdf_path="data/test_examples/temp_file.pdf" if content else None,
                            messages=messages,
                            threshold=0.4, top_k=3)

    # save the user message
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
