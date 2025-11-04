from fastapi import APIRouter, Request, UploadFile, File, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
import os

from team_lens_v1.services.rag.workflow_1_rag import rag_workflow_1
from team_lens_v1.services.rag.workflow_3_rag_chroma_trialusers import rag_workflow_3
from team_lens_v1.services.llm.prompt_settings import SYSTEM_PROMPT_TRIAL

from team_lens_v1.datamanager.models import TrialMessage
from team_lens_v1.datamanager.sql_datamanager import PostgresDataManager
from team_lens_v1.datamanager.sql_database_init import fastapi_sql_init


templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "templates"))
router = APIRouter()


@router.get("/trial", response_class=HTMLResponse)
def trial_page(request: Request):
    return templates.TemplateResponse("trial.html", {"request": request})


@router.post("/trial", response_class=HTMLResponse)
def trial_post(request: Request):
    pass

"""
better use annotation for File/Form/Depends

from typing import Annotated

file: Annotated[UploadFile | None, File(None)],
question: Annotated[str, Form(...)],
chat_id: Annotated[int | None, Form(None)],
session: Annotated[Session, Depends(fastapi_sql_init)]
"""
@router.post("/ask")
async def ask(
    file: UploadFile | None = File(None),
    question: str = Form(...),
    chat_id: int | None = Form(None),
    session: Session = Depends(fastapi_sql_init)
):
    import os
    import tempfile

    content = file.file.read() if file else None

    temp_pdf_path = None
    # Write a temporary file only if non-empty content was provided
    if content:
        fd, temp_pdf_path = tempfile.mkstemp(suffix=".pdf", prefix="team_lens_upload_")
        os.close(fd)
        with open(temp_pdf_path, "wb") as f:
            f.write(content)

    # call the function
    answer = rag_workflow_3(
        user_query=question,
        file_path=temp_pdf_path if content else None,
        top_k=3,
    )

    # Clean up temporary file
    if temp_pdf_path and os.path.exists(temp_pdf_path):
        try:
            os.remove(temp_pdf_path)
        except OSError:
            pass

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


@router.post("/ask/{chat_id}")
async def ask(
    chat_id: int,
    file: UploadFile | None = File(None),
    question: str = Form(...), # better go with question: Annotated[str, Form()] etc.
    session: Session = Depends(fastapi_sql_init),
):
    import os
    import tempfile

    content = await file.read() if file else None

    temp_pdf_path = None
    if content:
        fd, temp_pdf_path = tempfile.mkstemp(suffix=".pdf", prefix="team_lens_upload_")
        os.close(fd)
        with open(temp_pdf_path, "wb") as f:
            f.write(content)

    # get the latest 10 messages from the chat history and format them with system prompt
    data_manager = PostgresDataManager(session=session)
    chat_history = data_manager.get_trial_chat_history_by_id(chat_id)
    chat_history_system = [{"role": "system", "content": SYSTEM_PROMPT_TRIAL}]
    chat_history_formatted = (
        [{"role": "user" if msg.is_user else "assistant", "content": msg.text} for msg in chat_history]
        if chat_history
        else None
    )
    messages = chat_history_system + chat_history_formatted if chat_history_formatted else None

    # # call the function workflow 1
    # answer = rag_workflow_1(
    #     user_query=question,
    #     pdf_path=temp_pdf_path if content else None,
    #     messages=messages,
    #     threshold=0.4,
    #     top_k=3,
    # )

    # call the function workflow 3
    answer = rag_workflow_3(
        user_query=question,
        file_path=temp_pdf_path if content else None,
        messages=messages,
        top_k=3
    )

    # Clean up temporary file
    if temp_pdf_path and os.path.exists(temp_pdf_path):
        try:
            os.remove(temp_pdf_path)
        except OSError:
            pass

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
