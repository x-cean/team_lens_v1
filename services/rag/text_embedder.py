from config import OPENAI_API_KEY
from .parser import extract_text_from_pdf, extract_text_from_pdf_like_object
from openai import OpenAI
from typing import List


client = OpenAI(api_key=OPENAI_API_KEY)


def openai_text_embedder(text):
    """
    Uses OpenAI to embed text.
    :param text: The text to embed.
    :return: The embedding vector.
    """
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding
