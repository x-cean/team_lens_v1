import spacy
from sklearn.metrics.pairwise import cosine_similarity
from .parser import extract_text_from_pdf


# install a pretrained pipeline package
# python -m spacy download en_core_web_sm

# load the model
nlp = spacy.load("en_core_web_sm")


# tokenizing and chunking?
def text_to_chunks(text: str, chunk_size=100, overlap=20):
    pass


def text_to_sentences(text: str):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]


def embedding_list_of_strings(sentences: list[str]):
    sentence_vectors = [nlp(sentence).vector for sentence in sentences]
    return sentence_vectors


def embedding_string(text: str):
    return nlp(text).vector







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


example_pdf_path = "../../data/test_examples/Nature_moon.pdf"