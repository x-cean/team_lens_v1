from langchain.text_splitter import RecursiveCharacterTextSplitter


def recursive_char_text_split(text: str, chunk_size: int = 400, chunk_overlap: int = 0):
    """
    Splits the input text into chunks of specified size with optional overlap.
    """
    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", ". ", " ", ""], chunk_size = 600, chunk_overlap=0)
    docs = text_splitter.create_documents([text])
    return docs


def semantic_text_split(text: str, chunk_size: int = 400, chunk_overlap: int = 0):
    pass