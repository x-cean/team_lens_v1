import os
from typing import List
from pathlib import Path

from app.logger import logger
from app.config import CHROMA_PERSISTENT_DIR
from app.services.rag.parser_1 import docling_file_loader
from app.services.rag.vectordb_chroma_persistent import (collect_ids_and_documents_and_metadata_from_docs,
                                                         establish_chroma_persistent_client,
                                                         create_user_collection_with_openai_embedding,
                                                         add_documents_to_user_collection, query_collection)
from app.services.llm.open_ai_functions import get_response_from_openai


CHROMA_LOCAL_DATABASE_PATH = CHROMA_PERSISTENT_DIR
#todo: explore the chroma database, and improve the RAG retrieval!!!
# e.g. how to deal with it if all trials are in one collection.


def get_absolute_path(relative_path: str | Path) -> str:
    """
    Convert to absolute path, creating directories if needed.
    """
    path = Path(relative_path)
    if not path.is_absolute():
        path = path.resolve()
    path.mkdir(parents=True, exist_ok=True)
    return f"{path}"


def parse_file(file_path: str) -> tuple[List[str], List[str], List[dict]]:
    """
    Converts a PDF file to docs
    """
    # Extract content and create chunked docs
    docs = docling_file_loader(file_path)
    ids, docs, metadatas_list = collect_ids_and_documents_and_metadata_from_docs(docs)
    return ids, docs, metadatas_list


def embed_file_to_chroma_vector_db(file_path: str | None, user_id: str | None):
    """
    Embeds file content into Chroma vector database
    """
    # no file edge case
    if file_path is None:
        logger.info("No file path provided, skipping document addition to Chroma collection.")
        return

    chroma_client, chromadb_name, user_collection = get_chroma_collection(user_id)

    logger.info(f"File path provided: {file_path}, proceeding to add documents to Chroma collection.")
    # collect file embeddings if file_path is given
    ids, docs, metadatas_list = parse_file(file_path)
    # add documents to user collection
    add_documents_to_user_collection(client=chroma_client,
                                     user_id=chromadb_name,
                                     doc_ids=ids,
                                     doc_documents=docs,
                                     metadatas_list=metadatas_list)
    logger.info(f"Documents added to Chroma collection for user: {chromadb_name}")
    return user_collection


def get_chroma_collection(user_id: str | None):
    """
    connect to chroma persistent client and get or create user collection
    trial users all go to the same collection: "trial_user"
    users with user_id go to their own collection: user_id
    """
    # secure vector db path
    vector_db_path = get_absolute_path(CHROMA_LOCAL_DATABASE_PATH)
    # create path if not exist
    if not os.path.exists(vector_db_path):
        os.makedirs(vector_db_path)

    # determine chroma collection name
    if user_id is None:
        chromadb_name = "trial_user"
    else:
        chromadb_name = user_id

    # establish chroma persistent client
    chroma_client = establish_chroma_persistent_client(vector_db_path)
    # create or get user collection
    user_collection = create_user_collection_with_openai_embedding(client=chroma_client,
                                                                   user_id=chromadb_name)
    logger.info(f"Chroma collection ready: {user_collection.name}")
    return chroma_client, chromadb_name, user_collection


def rag_workflow_3(user_query: str,
                   file_path: str | None = None,
                   file_name: str | None = None,
                   user_id: str | None = None,
                   messages: List[dict] | None = None,
                   top_k: int = 3) -> str:

    user_collection = embed_file_to_chroma_vector_db(file_path, user_id)

    # query collection and get relevant text resources
    query_results = query_collection(collection=user_collection,
                                     query_text=user_query,
                                     n_results=top_k)

    # Chroma returns a dict with keys like 'documents', 'ids', 'metadatas'.
    # We safely extract the first list of documents (since we queried with a single text)
    documents = []
    if query_results:
        try:
            docs_field = query_results.get("documents")
            # docs_field is typically a list of lists, take the first query's result list
            if isinstance(docs_field, list) and docs_field:
                first_list = docs_field[0]
                if isinstance(first_list, list):
                    documents = first_list
        except Exception:
            # Leave documents empty if structure is unexpected
            documents = []

    if file_path and documents:
        text_resources = "\n".join(documents)
    elif file_path and not documents:
        text_resources = "File was given but no relevant info found."
    elif not file_path and documents:
        text_resources = ("User did not provide any file. "
                          "But based on previous documents added by trial user, here is some relevant info:\n" +
                          "\n".join(documents))
    else:
        text_resources = "User did not provide any file, and no relevant info found in the database."

    # Get response from OpenAI using the text resources
    answer = get_response_from_openai(user_prompt=user_query, resources=text_resources,
                                      model="gpt-5-mini", messages=messages)
    return answer






