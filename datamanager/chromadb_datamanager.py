import chromadb

from abc import ABC, abstractmethod
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
# todo: from chromadb.errors import what error?
from datetime import datetime

from team_lens_v1.config import OPENAI_API_KEY, CHROMA_API_KEY, CHROMA_TENANT_ID
from team_lens_v1.logger import logger


CHROMA_LOCAL_DATABASE_PATH = "/data/database/chroma_persistent"


class ChromadbDataManagerBase(ABC):
    def __init__(self, *, user_id: str):
        self.user_id = user_id
        if user_id is None:
            logger.error("Attempt to initiate PostgresDataManager without session")
            raise ValueError("Postgres session cannot be None")

    @abstractmethod
    def establish_client(self):
        pass

    def get_collection_if_exists(self, collection_name: str):
        client = self.establish_client()
        try:
            collection = client.get_collection(name=collection_name)
            return collection
        except Exception: # todo: change to the specific error
            return None

    def create_collection_with_openai_embedding(self, collection_name: str,
                                                file_path: str,
                                                doc_ids: list[str], doc_documents: list[str],
                                                metadatas_list: list[dict] = None):
        client = self.establish_client()
        logger.info(f"Creating collection {collection_name} for user {self.user_id}.")
        collection = client.get_or_create_collection(
            name=collection_name,
            embedding_function=OpenAIEmbeddingFunction(
                model_name="text-embedding-3-small",
                api_key=OPENAI_API_KEY
            ),
            metadata={
                "created_by": self.user_id,
                "created_at": str(datetime.now()),
                "source": file_path}
        )
        logger.info(f"Collection {collection_name} created successfully.")

        logger.info(f"Adding documents to collection {collection_name}.")
        collection.add(
            ids=doc_ids,
            documents=doc_documents,
            metadatas=metadatas_list
        )

        return collection

    def add_documents_to_collection(self, collection_name: str, ids, documents):
        collection = self.get_collection_if_exists(collection_name)
        if collection is None:
            logger.error(f"Collection {collection_name} does not exist.")
            raise ValueError(f"Collection {collection_name} does not exist.")
        else:
            logger.info(f"Adding documents to collection {collection_name}.")
            collection.add(
                ids=ids,
                documents=documents
            )
            return collection


class ChromadbPersistentDataManager(ChromadbDataManagerBase):
    def establish_client(self):
        user_chroma_client = chromadb.PersistentClient(path=f"{CHROMA_LOCAL_DATABASE_PATH}/{self.user_id}")
        return user_chroma_client


class ChromadbInMemoryDataManager(ChromadbDataManagerBase):
    def establish_client(self):
        user_chroma_client = chromadb.Client()
        return user_chroma_client


class ChromadbCloudDataManager(ChromadbDataManagerBase):
    def establish_client(self):
        user_chroma_client = chromadb.CloudClient(
            api_key=CHROMA_API_KEY,
            tenant=CHROMA_TENANT_ID,
            database='team_lens_db_1_development'
        )
        return user_chroma_client