from langchain.text_splitter import RecursiveCharacterTextSplitter


def recursive_char_text_split(text: str, chunk_size: int = 400, chunk_overlap: int = 0):
    """
    Splits the input text into chunks of specified size with optional overlap.
    """
    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", ". ", " ", ""],
                                                   keep_separator=False,
                                                   chunk_size = 600,
                                                   chunk_overlap=0)
    docs = text_splitter.create_documents([text])
    texts = [doc.page_content for doc in docs]
    return texts


### todo: specific text splitter, filtering metadata with help of llm
### todo: senmatic spliiter
### todo: dockling chunking


def semantic_text_split(text: str, chunk_size: int = 400, chunk_overlap: int = 0):
    pass