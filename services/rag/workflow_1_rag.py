from typing import List
from .parser import extract_text_from_pdf
from .text_chunkers import recursive_char_text_split
from .text_embedder import openai_text_embedder
from .cosine_similarity import similarity_matcher_skl


def file_embeddings(pdf_path: str, chunk_size: int = 600, chunk_overlap: int = 0) -> List[tuple[str, float]]:
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


def query_embedding(query: str) -> tuple[str, List[float]]:
    """
    Converts a user query to an embedding.
    """
    result = (query, openai_text_embedder(query))
    return result


def find_similarities(query_embedding: tuple[str, List[float]],
                      doc_embeddings: List[tuple[str, List[float]]]
                      ) -> List[tuple[str, float]]:
    """
    Finds the most similar document embeddings to the query embedding.
    """
    query_vector = query_embedding[1]
    similarities = []

    for doc, vector in doc_embeddings:
        # Calculate cosine similarity
        similarity = sum(q * d for q, d in zip(query_vector, vector)) / (sum(q ** 2 for q in query_vector) ** 0.5 * sum(d ** 2 for d in vector) ** 0.5)
        similarities.append((doc, similarity))

    # Sort by similarity score
    similarities.sort(key=lambda x: x[1], reverse=True)

    return similarities

