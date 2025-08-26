import chromadb
import os
import dotenv
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from config import OPENAI_API_KEY

# establish a persistent client for test purposes
chroma_client = chromadb.PersistentClient(path="/data/database/chroma")

# set up the embedding function
embedding_function = OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"
)

# create a collection
collection = chroma_client.create_collection(
    name="test_collection",
    embedding_function=embedding_function
)




