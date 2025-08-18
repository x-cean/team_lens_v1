from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple

def similarity_matcher_skl(query: tuple[str, List[float]], docs: List[Tuple[str, List[float]]]) -> List[tuple[str, float]]:
    docs_similarity_scores = []
    for doc in docs:
        similarity = cosine_similarity(query[1], doc[1])
        docs_similarity_scores.append((doc[0], similarity[0]))
    # Sort the documents by similarity score in descending order
    docs_similarity_scores.sort(key=lambda x: x[1], reverse=True)
    return docs_similarity_scores