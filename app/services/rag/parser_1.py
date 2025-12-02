"""
Langchain docling file loader and text extractor utilities
"""


from langchain_docling import DoclingLoader


def docling_file_loader(file_path: str):
    """
    Loads a file get its content, chunk and return as a list of langchain documents with langchain_docling
    """
    loader = DoclingLoader(file_path=file_path)
    docs = loader.load()
    for d in docs[:3]:
        print(f"- {d.page_content=}")
        print(type(d))
    return docs


def docs_to_texts(docs: list) -> list:
    """
    Converts a list of parsed langchain documents to a list of text strings
    """
    texts = [doc.page_content for doc in docs]
    return texts