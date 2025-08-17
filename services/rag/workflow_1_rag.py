from typing import List
from .parser import extract_text_from_pdf
from .text_chunkers import recursive_char_text_split
from .text_embedder import openai_text_embedder


def file_to_embeddings(pdf_path: str, chunk_size: int = 600, chunk_overlap: int = 0) -> List[tuple[str, float]]:
    """
    Converts a PDF file to a list of embeddings.
    """
    # Extract text from the PDF
    text = extract_text_from_pdf(pdf_path)

    # Split the text into chunks
    docs = recursive_char_text_split(text, chunk_size, chunk_overlap)

    # Embed each chunk using OpenAI
    results = [(doc, openai_text_embedder(doc)) for doc in docs]

    return results


def query_to_embedding(query: str) -> List[float]:
    """
    Converts a user query to an embedding.
    """
    return openai_text_embedder(query)

