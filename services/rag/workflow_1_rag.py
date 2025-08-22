import io
from typing import List
from .parser import extract_text_from_pdf, docling_file_loader, docs_to_texts
from .text_chunkers import recursive_char_text_split
from .text_embedder import openai_text_embedder
from .cosine_similarity import similarity_matcher_skl, cosine_similarity_manual, find_similar_items_manual
from ..llm.open_ai_functions import get_response_from_openai


def file_embeddings(file_path: str) -> List[tuple[str, List[float]]]:
    """
    Converts a PDF file to a list of embeddings.
    """
    # Extract content and create chunked docs
    docs = docling_file_loader(file_path)

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


# def find_similarities(query_embedding: tuple[str, List[float]],
#                       doc_embeddings: List[tuple[str, List[float]]],
#                       threshold=0.4, top_k=3) -> List[tuple[str, float]]:
#     """
#     Finds the most similar document embeddings to the query embedding.
#     """
#     sorted_similarities = find_similar_items_manual(query_embedding, doc_embeddings, threshold, top_k)
#     return sorted_similarities


def rag_workflow_1(user_query: str, pdf_path: str | io.BytesIO = None,
                     threshold: float = 0.4, top_k: int = 3) -> str:

    # If a file is given, embed it
    if pdf_path:
        query_emb = query_embedding(user_query)
        docs_embs = file_embeddings(pdf_path)
        similarities = find_similar_items_manual(query_emb, docs_embs, threshold, top_k)
        if similarities:
            text_resources = [doc for doc, score in similarities]
            text_resources = "\n".join(text_resources)
        else:
            text_resources = "File was given but no relevant info found."
    else:
        # If no file is given
        text_resources = "User did not provide any file."
    # Get response from OpenAI using the text resources
    answer = get_response_from_openai(user_prompt=user_query, resources=text_resources)
    return answer



