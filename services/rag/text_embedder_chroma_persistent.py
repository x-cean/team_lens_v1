import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from team_lens_v1.config import OPENAI_API_KEY


CHROMA_LOCAL_DATABASE_PATH = "/data/database/chroma_persistent"


def establish_chroma_persistent_client(user_id: str):
    user_chroma_client = chromadb.PersistentClient(path=f"{CHROMA_LOCAL_DATABASE_PATH}/{user_id}")
    return user_chroma_client

def create_collection_with_openai_embedding(user_id: str, collection_name: str,
                                            doc_ids: list[str], doc_documents: list[str]):
    client = establish_chroma_persistent_client(user_id)
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=OpenAIEmbeddingFunction(
            model_name="text-embedding-3-small"
        )
    )
    collection.add(
        ids=doc_ids,
        documents=doc_documents
    )
    return collection

def add_documents_to_collection(collection, ids, documents):
    collection.add(
        ids=ids,
        documents=documents
    )



