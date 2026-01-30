import hashlib


def sha256sum(filename):
    """
    Calculate SHA256 checksum for a given file.
    """
    h = hashlib.sha256()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()
