from typing import List
from .parser import extract_text_from_pdf, file_loader, docs_to_texts
from .text_chunkers import recursive_char_text_split
from .text_embedder import openai_text_embedder
from .cosine_similarity import similarity_matcher_skl, cosine_similarity_manual, find_similar_items_manual


def file_embeddings(file_path: str) -> List[tuple[str, List[float]]]:
    """
    Converts a PDF file to a list of embeddings.
    """
    # Extract content and create chunked docs
    docs = file_loader(file_path)

    # Turn docs into text strings
    texts = docs_to_texts(docs)

    # Embed each chunk using OpenAI
    results = [(text, openai_text_embedder(text)) for text in texts]

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
    sorted_similarities = find_similar_items_manual(query_embedding, doc_embeddings, threshold, top_k)
    return sorted_similarities


def rag_workflow_1(pdf_path: str, user_query: str,
                   chunk_size: int = 600, chunk_overlap: int = 0,
                     threshold: float = 0.4, top_k: int = 3) -> List[tuple[str, float]]:
    docs_embs = file_embeddings(pdf_path)
    query_emb = query_embedding(user_query)
    similarities = find_similarities(query_emb, docs_embs, threshold, top_k)


