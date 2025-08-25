import chromadb


chroma_client = chromadb.PersistentClient(path="/data/database/chroma")

collection = chroma_client.create_collection(name="test_collection")


