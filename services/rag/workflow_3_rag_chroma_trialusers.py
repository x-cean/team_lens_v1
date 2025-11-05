import os
from typing import List
from pathlib import Path

from team_lens_v1.logger import logger
from team_lens_v1.services.rag.parser_1 import docling_file_loader
from team_lens_v1.services.rag.vectordb_chroma_persistent import (collect_ids_and_documents_and_metadata_from_docs,
                                                                  establish_chroma_persistent_client,
                                                                  create_user_collection_with_openai_embedding,
                                                                  add_documents_to_user_collection, query_collection)
from team_lens_v1.services.llm.open_ai_functions import get_response_from_openai


CHROMA_LOCAL_DATABASE_PATH = Path(__file__).parent.parent.parent.parent / "data_storage" / "chroma_db" / "chroma_persistent"



def get_absolute_path(relative_path: str | Path) -> str:
    """Convert to absolute path, creating directories if needed."""
    path = Path(relative_path)
    if not path.is_absolute():
        path = path.resolve()
    path.mkdir(parents=True, exist_ok=True)
    return f"{path}"


def file_embeddings(file_path: str) -> tuple[List[str], List[str], List[dict]]:
    """
    Converts a PDF file to docs
    """
    # Extract content and create chunked docs
    docs = docling_file_loader(file_path)
    ids, docs, metadatas_list = collect_ids_and_documents_and_metadata_from_docs(docs)
    return ids, docs, metadatas_list


def rag_workflow_3(user_query: str, file_path: str = None,
                   user_id: str = None,
                   messages: List[dict] = None,
                   top_k: int = 3) -> str:

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


    if file_path is None:
        logger.info("No file path provided, skipping document addition to Chroma collection.")
    else:
        logger.info(f"File path provided: {file_path}, proceeding to add documents to Chroma collection.")
        # collect file embeddings if file_path is given
        ids, docs, metadatas_list = file_embeddings(file_path)
        # add documents to user collection
        add_documents_to_user_collection(client=chroma_client,
                                         user_id=chromadb_name,
                                         doc_ids=ids,
                                         doc_documents=docs,
                                         metadatas_list=metadatas_list)
        logger.info(f"Documents added to Chroma collection for user: {chromadb_name}")

    # query collection and get relevant text resources
    query_results = query_collection(collection=user_collection,
                                     query_text=user_query,
                                     n_results=top_k)
    if file_path and query_results:
        text_resources = "\n".join(query_results)
    elif file_path and not query_results:
        text_resources = "File was given but no relevant info found."
    elif not file_path and query_results:
        text_resources = ("User did not provide any file. "
                          "But based on previous documents added by trial user, here is some relevant info:\n")
    else:
        text_resources = "User did not provide any file, and no relevant info found in the database."

    # Get response from OpenAI using the text resources
    answer = get_response_from_openai(user_prompt=user_query, resources=text_resources,
                                      model="gpt-5-mini", messages=messages)
    return answer



