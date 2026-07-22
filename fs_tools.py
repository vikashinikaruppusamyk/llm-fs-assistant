import os
from pypdf import PdfReader
from docx import Document
from datetime import datetime

def read_file(filepath: str) -> dict:
    """
    Reads a file and returns its text content along with metadata.

    Args:
        filepath: Path to the file (.txt, .pdf, or .docx)

    Returns:
        A dictionary with keys:
            success (bool)
            content (str or None)
            error (str or None)
            metadata (dict) - filename, extension, size in bytes
    """
    if not os.path.exists(filepath):
        return {
            "success": False,
            "content": None,
            "error": f"File not found: {filepath}",
            "metadata": {}
        }

    _, extension = os.path.splitext(filepath)
    extension = extension.lower()

    try:
        if extension == ".txt":
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

        elif extension == ".pdf":
            reader = PdfReader(filepath)
            pages_text = []
            for page in reader.pages:
                pages_text.append(page.extract_text() or "")
            content = "\n".join(pages_text)

        elif extension == ".docx":
            doc = Document(filepath)
            paragraphs = [p.text for p in doc.paragraphs]
            content = "\n".join(paragraphs)

        else:
            return {
                "success": False,
                "content": None,
                "error": f"Unsupported file type: {extension}",
                "metadata": {}
            }

        metadata = {
            "filename": os.path.basename(filepath),
            "extension": extension,
            "size_bytes": os.path.getsize(filepath)
        }

        return {
            "success": True,
            "content": content,
            "error": None,
            "metadata": metadata
        }

    except Exception as e:
        return {
            "success": False,
            "content": None,
            "error": str(e),
            "metadata": {}
        }

def list_files(directory: str, extension: str = None) -> list:
    """
    Lists files in a directory, optionally filtered by extension.

    Args:
        directory: Path to the directory to scan
        extension: Optional filter, e.g. '.pdf', '.txt' (case-insensitive)

    Returns:
        A list of dicts, each with:
            name (str)
            path (str) - full path to the file
            size_bytes (int)
            modified (str) - last modified timestamp
    """
    if not os.path.isdir(directory):
        return []

    results = []

    for filename in os.listdir(directory):
        full_path = os.path.join(directory, filename)

        # Skip subdirectories - we only want files
        if not os.path.isfile(full_path):
            continue

        # Apply extension filter if provided
        if extension:
            if not filename.lower().endswith(extension.lower()):
                continue

        stats = os.stat(full_path)

        results.append({
            "name": filename,
            "path": full_path,
            "size_bytes": stats.st_size,
            "modified": datetime.fromtimestamp(stats.st_mtime).isoformat()
        })

    return results


def write_file(filepath: str, content: str) -> dict:
    """
    Writes content to a file, creating parent directories if needed.

    Args:
        filepath: Destination path for the file
        content: Text content to write

    Returns:
        A dictionary with keys:
            success (bool)
            error (str or None)
            filepath (str) - the path written to
    """
    try:
        # Step 1: Figure out the parent directory
        parent_dir = os.path.dirname(filepath)

        # Step 2: Create it if it doesn't exist (and isn't empty, e.g. same-folder path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        # Step 3: Write the content
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return {
            "success": True,
            "error": None,
            "filepath": filepath
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "filepath": filepath
        }

def search_in_file(filepath: str, keyword: str) -> dict:
    """
    Searches for a keyword inside a file's content (case-insensitive)
    and returns matches with surrounding context.

    Args:
        filepath: Path to the file to search
        keyword: The word/phrase to search for

    Returns:
        A dictionary with keys:
            success (bool)
            found (bool) - whether any match was found
            matches (list) - list of context snippets
            error (str or None)
    """
    # Reuse read_file so we don't duplicate format-handling logic
    file_result = read_file(filepath)

    if not file_result["success"]:
        return {
            "success": False,
            "found": False,
            "matches": [],
            "error": file_result["error"]
        }

    content = file_result["content"]
    content_lower = content.lower()
    keyword_lower = keyword.lower()

    matches = []
    context_chars = 50  # characters of context on each side

    start = 0
    while True:
        idx = content_lower.find(keyword_lower, start)
        if idx == -1:
            break

        snippet_start = max(0, idx - context_chars)
        snippet_end = min(len(content), idx + len(keyword) + context_chars)
        snippet = content[snippet_start:snippet_end]

        matches.append(snippet.strip())
        start = idx + len(keyword)

    return {
        "success": True,
        "found": len(matches) > 0,
        "matches": matches,
        "error": None
    }