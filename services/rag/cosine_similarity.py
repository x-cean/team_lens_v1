import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple
from team_lens_v1.logger import logger


### todo: vector database


def similarity_matcher_skl(query: tuple[str, List[float]], docs: List[Tuple[str, List[float]]]) -> List[tuple[str, float]]:
    docs_similarity_scores = []
    for doc in docs:
        similarity = cosine_similarity(query[1], doc[1])
        docs_similarity_scores.append((doc[0], similarity[0]))
    # Sort the documents by similarity score in descending order
    docs_similarity_scores.sort(key=lambda x: x[1], reverse=True)
    return docs_similarity_scores


def cosine_similarity_manual(vec1, vec2):
    """Calculate the cosine similarity between two vectors."""
    vec1 = np.array(vec1, dtype=float)
    vec2 = np.array(vec2, dtype=float)


    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)


def find_similar_items_manual(query, docs, threshold=0.4, top_k=3):
    """Find the most similar items based on cosine similarity."""
    docs_similarity_scores = []
    for doc in docs:
        similarity = cosine_similarity_manual(query[1], doc[1])
        docs_similarity_scores.append((doc[0], similarity))
    # Sort the documents by similarity score in descending order
    docs_similarity_scores.sort(key=lambda x: x[1], reverse=True)
    # Log info of 3 most similar documents session found
    for doc, similarity in docs_similarity_scores[:3]:
        logger.info(f"Text: {doc[:100]}, Similarity Score: {similarity}.4f")# Log first 100 characters of each doc
    # Filter out items below the threshold
    filtered_results = \
        [(doc, score) for doc, score in docs_similarity_scores if score > threshold][:top_k]
    return filtered_results
