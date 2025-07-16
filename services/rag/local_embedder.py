import spacy
from sklearn.metrics.pairwise import cosine_similarity
from .parser import extract_text_from_pdf


# install a pretrained pipeline package
# python -m spacy download en_core_web_sm

# load the model
nlp = spacy.load("en_core_web_sm")

# documents
docs = [
    "CRISPR is a powerful tool for gene editing.",
    "GPT-4 is a state-of-the-art language model.",
]

# embed documents
doc_vectors = [nlp(doc).vector for doc in docs]

# embed query
query = "Tell me about CRISPR."
query_vector = nlp(query).vector

# compare similarity
similarities = cosine_similarity([query_vector], doc_vectors)
best_idx = similarities[0].argmax()
print("Most relevant doc:", docs[best_idx])