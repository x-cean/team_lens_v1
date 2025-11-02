from markitdown import MarkItDown


def parse_file_from_path_markitdown(file_path: str):
    md = MarkItDown(enable_plugins=False) # Set to True to enable plugins
    result = md.convert(file_path)
    return result.text_content

