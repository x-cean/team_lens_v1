import os
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from .parser import extract_text_from_pdf, extract_text_from_pdf_like_object
from ..llm.germini_functions import get_response_from_germini


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

    # collect the sentences in a list
    matched_sentences = [i[0] for i in good_matches]

    return matched_sentences


def simple_rag_pipeline(doc: str, user_query: str):
    """
    A function ready to be called from fastapi
    """
    results = find_similarity_of_query_from_one_doc(user_query, doc)
    result_text = " ".join(results)
    response = get_response_from_germini(result_text, user_query)
    return response


def main():
    base_dir = os.path.dirname(__file__)
    example_pdf_path = os.path.join(base_dir, "../../data/test_examples/Nature_moon.pdf")
    example_pdf_path = os.path.abspath(example_pdf_path)

    doc = extract_text_from_pdf(example_pdf_path)
    user_query = "What is this article mainly about? What did the scientists find in the dark side of the moon?"
    results = find_similarity_of_query_from_one_doc(user_query, doc)
    result_text = " ".join(results) # join a list of str

    print(get_response_from_germini(result_text, user_query))



if __name__ == "__main__":
    main()



"""
Germini:
This article is mainly about:

*   The investigation by Zhou and colleagues, using samples from the Chang'e-6 mission, into how lunar asymmetry manifested in the far-side mantle.
*   Whether there is evidence that the impact that formed the SPA basin influenced this lunar asymmetry.

Regarding what the scientists found in the "dark side" of the moon:

*   The article clarifies that the part of the Moon that faces away from Earth is more accurately called the 'far side' and receives just as much sunlight as the side we can see, so it's not truly 'dark'.
*   Regarding findings from the far-side samples, the text states that a valid interpretation of the data suggests that a physical mechanism caused the near side of the lunar magma ocean to behave differently from the far side. It also points to an intriguing possibility that the SPA impact directly affected the deep interior of the Moon. The article discusses what the data suggests and implies, rather than presenting a final, conclusive finding.
"""


