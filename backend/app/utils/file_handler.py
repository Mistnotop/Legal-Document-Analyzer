from pathlib import Path


def ensure_directory(directory: Path):
    directory.mkdir(parents=True, exist_ok=True)