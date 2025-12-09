from fastapi import APIRouter, Request, UploadFile, File, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
import os
import re

from app.services.rag.workflow_3_rag_chroma_trial_users import rag_workflow_3, embed_file_to_chroma_vector_db
from app.services.llm.prompt_settings import SYSTEM_PROMPT_TRIAL

from app.datamanager.models_trial_users import TrialMessage, TrialFile
from app.datamanager.sql_trial_datamanager import TrialSQLDataManager
from app.datamanager.sql_database_init import fastapi_sql_init


templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "templates"))
router = APIRouter()


@router.get("/trial", response_class=HTMLResponse)
def trial_page(request: Request):
    return templates.TemplateResponse("trial.html", {"request": request})


@router.post("/trial", response_class=HTMLResponse)
def trial_post(request: Request):
    pass


@router.post("/create-chat")
async def create_chat(session: Session = Depends(fastapi_sql_init)):
    """
    Create a new trial chat session and return its ID.
    Called when the trial page loads.
    """
    data_manager = TrialSQLDataManager(session=session)
    new_chat = data_manager.create_trial_chat()

    return JSONResponse({
        "chat_id": new_chat.id
    })


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    chat_id: int = Form(...),
    session: Session = Depends(fastapi_sql_init)
):
    """
    Accept a file upload and save it temporarily using its original name.
    Add that file information to SQL.
    """
    import tempfile

    # Sanitize the filename to avoid directory traversal and unsafe chars
    original_name = os.path.basename(file.filename or "uploaded_file")
    name, ext = os.path.splitext(original_name)
    # allow letters, numbers, dash, underscore, dot in base name
    safe_name = re.sub(r"[^A-Za-z0-9._-]", "_", name).strip("._-") or "file"
    safe_filename = safe_name + ext

    # Create a unique temp directory to avoid collisions while keeping original name
    temp_dir = tempfile.mkdtemp(prefix="team_lens_upload_")
    save_path = os.path.join(temp_dir, safe_filename)

    content = await file.read()
    with open(save_path, "wb") as f:
        f.write(content)

    # Embed the file into Chroma vector DB for trial users
    embed_file_to_chroma_vector_db(file_path=save_path, user_id=None)

    # Create TrialFile record
    trial_file = TrialFile(
        file_name=original_name,
        file_path=save_path,
        chat_id=chat_id
    )
    session.add(trial_file)
    session.commit()

    return JSONResponse({
        "action": "file uploaded and embedded",
        "file_path": save_path,
        "original_name": original_name
    })


@router.post("/ask")
async def ask(
    chat_id: int = Form(...),
    question: str = Form(...),  # better go with question: Annotated[str, Form()] etc. ?
    session: Session = Depends(fastapi_sql_init),
):
    # get the latest 10 messages from the chat history and format them with system prompt
    data_manager = TrialSQLDataManager(session=session)
    chat_history = data_manager.get_trial_chat_history_by_id(chat_id)
    chat_history_system = [{"role": "system", "content": SYSTEM_PROMPT_TRIAL}]
    chat_history_formatted = (
        [{"role": "user" if msg.is_user else "assistant", "content": msg.text} for msg in chat_history]
        if chat_history
        else None
    )
    # combine system prompt and chat history if any, else just None because my openai function can handle that
    messages = chat_history_system + chat_history_formatted if chat_history_formatted else None

    # check whether any file is associated with this chat
    trial_files = data_manager.get_trial_files_by_chat_id(chat_id)
    if trial_files:
        file_name = trial_files[-1].file_name  #todo: assume only last uploaded file per trial chat for now
    else:
        file_name = None
    # call the function workflow 3
    answer = rag_workflow_3(
        user_query=question,
        messages=messages,
        top_k=3,
        file_name=file_name
    )

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
