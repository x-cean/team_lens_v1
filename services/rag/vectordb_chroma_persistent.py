import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from datetime import datetime
from team_lens_v1.config import OPENAI_API_KEY


CHROMA_LOCAL_DATABASE_PATH = "/data/database/chroma_persistent"


def collect_ids_and_documents_and_metadata_from_docs(docs, user_id: str | None=None,
                                                     workspace_id: str | None=None):
    """
    downstream step after document loading with docling
    Collects ids, documents, and metadata from a list of Document objects
    important step where metadata such as source is added
    """
    ids = []
    documents = []
    metadatas_list = []
    for i, doc in enumerate(docs):
        ids.append(f"{i}")
        documents.append(doc.page_content)
        metadata_dict = {"source": doc.metadata.get("source", "unknown")}
        if workspace_id:
            metadata_dict["workspace_id"] = workspace_id
        if user_id:
            metadata_dict["user_id"] = user_id
        metadatas_list.append(metadata_dict)
    return ids, documents, metadatas_list

def establish_chroma_persistent_client():
    user_chroma_client = chromadb.PersistentClient(path=f"{CHROMA_LOCAL_DATABASE_PATH}")
    return user_chroma_client

def get_user_collection_if_exists(user_id: str):
    client = establish_chroma_persistent_client()
    try:
        collection = client.get_collection(name=user_id)
        return collection
    except Exception as e: # todo: figure out the specific error
        return e

def create_user_collection_with_openai_embedding(user_id: str):
    client = establish_chroma_persistent_client()
    collection = client.get_or_create_collection(
        name=user_id,
        embedding_function=OpenAIEmbeddingFunction(
            model_name="text-embedding-3-small",
            api_key=OPENAI_API_KEY
        ),
        metadata={
            "created_at": str(datetime.now()),
            "source": "user_collection"}
    )
    return collection

def add_documents_to_collection(user_id: str,
                                doc_ids: list[str],
                                doc_documents: list[str],
                                metadatas_list: list[dict] = None):
    collection = get_user_collection_if_exists(user_id)
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




