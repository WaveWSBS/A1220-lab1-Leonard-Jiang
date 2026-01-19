# file_io.py
import os
import base64

def encode_file(path):
    """Encode a file's contents as base64 text.

    Args:
        path (str): Path to the file to encode.

    Returns:
        str: Base64-encoded contents of the file.

    Assumptions:
        The file exists and is readable as binary data.
    """
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def list_files(dirpath):
    """Yield file names and paths within a directory.

    Args:
        dirpath (str): Path to the directory to scan.

    Yields:
        Tuple[str, str]: The file name and full file path for each file.

    Assumptions:
        The directory exists; subdirectories are ignored.
    """
    for name in os.listdir(dirpath):
        path = os.path.join(dirpath, name)
        if os.path.isfile(path):
            yield name, path
