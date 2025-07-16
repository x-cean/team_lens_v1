import os
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from .parser import extract_text_from_pdf


# install a pretrained pipeline package
# python -m spacy download en_core_web_sm

# load the model
nlp = spacy.load("en_core_web_sm")


# tokenizing and chunking?
def text_to_chunks(text: str, chunk_size=100, overlap=20): # unify chunk size
    pass


def text_to_sentences(text: str): # break long text to sentences, works for single file for now
    sentences = [sent.text for sent in nlp(text).sents]
    return sentences


def embedding_list_of_strings(sentences: list[str]):
    sentence_vectors = [nlp(sentence).vector for sentence in sentences]
    return sentence_vectors


def embedding_string(text: str):
    return nlp(text).vector


def find_similarity_of_query_from_one_doc(user_query: str, doc: str):
    # create a list of sentences
    sentences = text_to_sentences(doc)

    # embedding
    doc_vectors = embedding_list_of_strings(sentences)
    query_vector = nlp(user_query).vector

    # compare
    similarity = cosine_similarity([query_vector], doc_vectors)[0]

    # sorting
    ranked_indices = similarity.argsort()[::-1]

    # get a list of good enough results: sentences and similarity scores, threshold is for now 0.2
    good_matches = [(sentences[idx], similarity[idx]) for idx in ranked_indices if similarity[idx] > 0.2]

    # keep up to 5 best matches
    good_matches = good_matches[:5]

    matched_sentences = [i[0] for i in good_matches]

    return matched_sentences


def main():
    base_dir = os.path.dirname(__file__)
    example_pdf_path = os.path.join(base_dir, "../../data/test_examples/Nature_moon.pdf")
    example_pdf_path = os.path.abspath(example_pdf_path)

    doc = extract_text_from_pdf(example_pdf_path)
    user_query = "What is this article mainly about? What did the scientists find in the dark side of the moon?"
    results = find_similarity_of_query_from_one_doc(user_query, doc)
    print(results)



if __name__ == "__main__":
    main()
