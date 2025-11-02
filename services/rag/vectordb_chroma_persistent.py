import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from datetime import datetime
from team_lens_v1.config import OPENAI_API_KEY


CHROMA_LOCAL_DATABASE_PATH = "/data/database/chroma_persistent"


def collect_ids_and_documents_and_metadata_from_docs(docs, user_id: str | None=None):
    ids = []
    documents = []
    metadata_list = []
    for i, doc in enumerate(docs):
        ids.append(f"{i}")
        documents.append(doc.page_content)
        metadata_list.append({"username": user_id, "source": doc.metadata.get("source", "unknown")})
    return ids, documents, metadata_list

def establish_chroma_persistent_client(user_id: str):
    user_chroma_client = chromadb.PersistentClient(path=f"{CHROMA_LOCAL_DATABASE_PATH}/{user_id}")
    return user_chroma_client


def get_collection_if_exists(user_id: str, collection_name: str):
    client = establish_chroma_persistent_client(user_id)
    try:
        collection = client.get_collection(name=collection_name)
        return collection
    except chromadb.errors.CollectionNotFoundError:
        return None

def create_collection_with_openai_embedding(user_id: str, collection_name: str,
                                            file_path: str,
                                            doc_ids: list[str], doc_documents: list[str],
                                            metadata_list: list[dict] = None):
    client = establish_chroma_persistent_client(user_id)
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=OpenAIEmbeddingFunction(
            model_name="text-embedding-3-small"
        ),
        metadata={
            "created_by": user_id,
            "created_at": str(datetime.now()),
            "source": file_path}
    )
    collection.add(
        ids=doc_ids,
        documents=doc_documents,
        metadatas=metadata_list
    )
    return collection


def add_documents_to_collection(collection, ids, documents):
    collection.add(
        ids=ids,
        documents=documents
    )
    return collection



