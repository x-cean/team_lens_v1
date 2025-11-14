from markitdown import MarkItDown

from docling_core.types.doc import DoclingDocument, TextItem, NodeItem
from docling_core.types.doc.document import DocItemLabel


def parse_file_from_path_markitdown(file_path: str) -> str:
    md = MarkItDown(enable_plugins=False) # Set to True to enable plugins
    result = md.convert(file_path)
    return result.text_content


def text_to_docling_document(text: str) -> DoclingDocument:
    """Convert plain text to a DoclingDocument with a single text node."""
    doc = DoclingDocument(name="text_document")

    # Create a text item with the content
    text_item = TextItem(text=text)

    # Add it as a paragraph node
    doc.add_text(
        label=DocItemLabel.PARAGRAPH,
        text=text
    )
    return doc



