from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker

def parse_and_chunk_pdf(file_path: str, max_tokens: int = 500):
    """Parse PDF and chunk semantically using Docling v2."""
    # Step 1: Parse PDF to DoclingDocument (preserves structure automatically)
    converter = DocumentConverter()
    result = converter.convert(file_path)
    doc = result.document  # Already a DoclingDocument with semantic labels

    # Step 2: Chunk semantically
    chunker = HybridChunker()
    chunks = chunker.chunk(doc)

    return [chunk.text for chunk in chunks]
