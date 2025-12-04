import chromadb
import os

from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from datetime import datetime


def create_persistent_db_folder_if_not_exist(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def collect_ids_and_documents_and_metadata_from_docs(docs, user_id: str | None=None,
                                                     workspace_id: str | None=None):
    """
    downstream step after document loading with langchain docling loader
    Collects ids, documents, and metadata from a list of Document objects
    important step where metadata such as source is added
    """
    ids = []
    documents = []
    metadatas_list = []
    for i, doc in enumerate(docs):
        ids.append(f"{i + 1}")
        documents.append(doc.page_content)
        metadata_dict = {"source": doc.metadata.get("source", "unknown"),
                         "filename": doc.metadata["dl_meta"]["origin"]["filename"] \
                             if ("dl_meta" in doc.metadata and "origin" in doc.metadata["dl_meta"]
                                 and "filename" in doc.metadata["dl_meta"]["origin"]) \
                             else "unknown",
                         "headings": doc.metadata["dl_meta"]["headings"] \
                         if ("dl_meta" in doc.metadata and "headings" in doc.metadata) \
                         else []}
        if workspace_id:
            metadata_dict["workspace_id"] = workspace_id
        if user_id:
            metadata_dict["user_id"] = user_id
        metadatas_list.append(metadata_dict)
    return ids, documents, metadatas_list

def collect_ids_and_chunks_and_metadata_from_chunks(chunks):
    """
    downstream step after document loading with docling converter and then hybrid chunker
    Collects ids, documents, and metadata from a list of Document objects
    important step where metadata such as source is added
    """
    ids = []
    chunks = []
    metadatas_list = []
    for i, chunk in enumerate(chunks):
        ids.append(f"{i + 1}")
        chunks.append(chunk.text)
        metadata_dict = dict(chunk.meta) if chunk.meta else {} # chunk.data is an object so need to convert to dict
        metadatas_list.append(metadata_dict)
    return ids, chunks, metadatas_list
    # todo: remember how to collect metadata from chunk.meta (refer to test2, get headers and sources)

def establish_chroma_persistent_client(path):
    path = create_persistent_db_folder_if_not_exist(path)
    user_chroma_client = chromadb.PersistentClient(path=path)
    return user_chroma_client

def get_user_collection_if_exists(client, user_id: str):
    try:
        collection = client.get_collection(name=user_id)
        return collection
    except Exception as e: # todo: figure out the specific error
        return e

def get_or_create_user_collection_with_openai_embedding(client, user_id: str):
    collection = client.get_or_create_collection(
        name=user_id,
        embedding_function=OpenAIEmbeddingFunction(
            model_name="text-embedding-3-small",
        ),
        metadata={
            "created_at": str(datetime.now()),
            "source": "user_collection"}
    )
    return collection

def add_documents_to_user_collection(client,
                                user_id: str,
                                doc_ids: list[str],
                                doc_documents: list[str],
                                metadatas_list: list[dict] = None):
    collection = get_user_collection_if_exists(client, user_id)
    collection.add(
        ids=doc_ids,
        documents=doc_documents,
        metadatas=metadatas_list
    )
    return collection

def query_collection(collection, query_text: str, n_results: int = 3):
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    return results




