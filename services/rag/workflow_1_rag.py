from typing import List
from .parser import extract_text_from_pdf
from .text_chunkers import recursive_char_text_split
from .text_embedder import openai_text_embedder
from .cosine_similarity import similarity_matcher_skl


def file_embeddings(pdf_path: str, chunk_size: int = 600, chunk_overlap: int = 0) -> List[tuple[str, List[float]]]:
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
                      doc_embeddings: List[tuple[str, List[float]]],
                      threshold=0.5, top_k=2) -> List[tuple[str, float]]:
    """
    Finds the most similar document embeddings to the query embedding.
    """
    sorted_similarities = similarity_matcher_skl(query_embedding, doc_embeddings)

    # Filter results based on the threshold and select top_k results
    similarity_matches = [(doc, score) for doc, score in sorted_similarities if score > threshold]
    similarity_matches = similarity_matches[:top_k]
    return similarity_matches


def rag_workflow_1(pdf_path: str, user_query: str,
                   chunk_size: int = 600, chunk_overlap: int = 0,
                     threshold: float = 0.5, top_k: int = 2) -> List[tuple[str, float]]:
    docs_embs = file_embeddings(pdf_path)
    query_emb = query_embedding(user_query)
    similarities = find_similarities(query_emb, docs_embs, threshold, top_k)

