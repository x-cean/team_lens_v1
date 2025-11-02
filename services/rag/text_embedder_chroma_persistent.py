import chromadb


CHROMA_LOCAL_DATABASE_PATH = "/data/database/chroma_persistent"


def establish_chroma_persistent_client(user_id: str):
    user_chroma_client = chromadb.PersistentClient(path=f"{CHROMA_LOCAL_DATABASE_PATH}/{user_id}")
    return user_chroma_client


