import chromadb
import os
import dotenv
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from config import OPENAI_API_KEY

chroma_client = chromadb.PersistentClient(path="/data/database/chroma")

collection = chroma_client.create_collection(
    name="test_collection",
    embedding_function=OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-small"
    )
)


