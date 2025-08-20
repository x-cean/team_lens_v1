from pypdf import PdfReader
from langchain_docling import DoclingLoader


def file_loader(file_path: str):
    """
    Loads a file get its content, chunk and return as a list of langchain documents with langchain_docling
    """
    loader = DoclingLoader(file_path=file_path)
    docs = loader.load()
    for d in docs[:3]:
        print(f"- {d.page_content=}")
        print(type(d))
    return docs


def docs_to_texts(docs: list) -> list:
    """
    Converts a list of parsed langchain documents to a list of text strings
    """
    texts = [doc.page_content for doc in docs]
    return texts


def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PdfReader(file)
            page_texts = [page.extract_text() or "" for page in reader.pages]
        text = " ".join(page_texts)
        return text.replace("\n", "")
    except FileNotFoundError:
        return "File not found"


def extract_text_from_pdf_like_object(pdf_like_object):
    text = ""
    try:
        reader = PdfReader(pdf_like_object)
        page_texts = [page.extract_text() or "" for page in reader.pages]
        text = " ".join(page_texts)
        return text.replace("\n", " ")
    except FileNotFoundError:
        return "File not found"


def extract_text_from_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "File not found"


# example_pdf_path = "../../data/test_examples/Nature_moon.pdf"
# text = extract_text_from_pdf(example_pdf_path)
# print(text)