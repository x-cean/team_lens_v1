from pypdf import PdfReader


def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PdfReader(file)
            page_texts = [page.extract_text() or "" for page in reader.pages]
        text = " ".join(page_texts)
        return text.replace("\n", " ")
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