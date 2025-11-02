import chromadb

from abc import ABC, abstractmethod
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from datetime import datetime

from team_lens_v1.config import OPENAI_API_KEY
from team_lens_v1.logger import logger


CHROMA_LOCAL_DATABASE_PATH = "/data/database/chroma_persistent"


class ChromadbDataManagerBase(ABC):
    def __init__(self, *, user_id: str):
        self.user_id = user_id
        if user_id is None:
            logger.error("Attempt to initiate PostgresDataManager without session")
            raise ValueError("Postgres session cannot be None")

    @abstractmethod
    def connect(self):
        pass

    def disconnect(self):
        pass

    def add_data(self, data):
        pass

    def get_data(self, query):
        pass