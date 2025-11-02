import io
import os
from typing import List
from .parser_1 import extract_text_from_pdf, docling_file_loader, docs_to_texts
from .text_chunkers import recursive_char_text_split
from .text_embedder import openai_text_embedder
from .cosine_similarity import similarity_matcher_skl, cosine_similarity_manual, find_similar_items_manual
from ..llm.open_ai_functions import get_response_from_openai


def get_all_file_paths(path: str) -> List[str]:
    """
    Collects file paths from a given path.
    """
    file_paths = []
    if os.path.isfile(path):
        file_paths.append(path)
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)
    else:
        print(f"Error: Provided path '{path}' is not a valid file or directory.")
    return file_paths


def file_embeddings(file_path: str) -> List[tuple[str, List[float]]]:
    """
    Converts a file to a list of embeddings.
    The output list's index can be used as chunk index: for index, result in enumerate(results)
    """
    # Extract content and create chunked docs
    docs = docling_file_loader(file_path)

    # Turn docs into text strings
    texts = docs_to_texts(docs)

    # Embed each chunk using OpenAI, if texts is a list of strings
    results = [(text, openai_text_embedder(text)[0].embedding) for text in texts]
    return results


def query_embedding(query: str) -> tuple[str, List[float]]:
    """
    Converts a user query to an embedding.
    """
    embedding_result = openai_text_embedder(query)[0].embedding
    result = (query, embedding_result)
    return result


def rag_workflow_2(user_query: str, resource_file: str | io.BytesIO = None,
                     threshold: float = 0.4, top_k: int = 3) -> str:

    # If a file is given, embed it
    if resource_file:
        query_emb = query_embedding(user_query)
        docs_embs = file_embeddings(resource_file)
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



