from pathlib import Path
import re
from html.parser import HTMLParser

import fitz
import pandas as pd

from app.core.config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    ALLOWED_CLASSES,
)


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        data = data.strip()
        if data:
            self.parts.append(data)

    def text(self) -> str:
        return " ".join(self.parts)


def clean_text(text: str) -> str:
    text = str(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def read_contract_text(local_path: str) -> str:
    path = RAW_DATA_DIR / local_path

    if path.suffix.lower() == ".pdf":
        text = ""
        with fitz.open(path) as pdf:
            for page in pdf:
                text += page.get_text()
        return text

    content = path.read_text(encoding="utf-8", errors="ignore")

    if path.suffix.lower() in {".html", ".htm"}:
        parser = TextExtractor()
        try:
            parser.feed(content)
            return parser.text()
        except AssertionError:
            return content

    return content


def main():

    metadata_path = RAW_DATA_DIR / "downloaded_contracts_metadata.csv"

    print("Loading metadata...")

    df = pd.read_csv(
        metadata_path,
        low_memory=False
    )

    print(f"Total records: {len(df)}")

    df = df[
        df["label"].isin(ALLOWED_CLASSES)
    ]

    print(f"Selected records: {len(df)}")

    df = df[
        ["local_path", "label"]
    ].copy()

    df.dropna(inplace=True)

    print("Reading downloaded contract files...")

    df["text"] = df["local_path"].apply(read_contract_text)
    df["text"] = df["text"].apply(clean_text)

    df = df[
        df["text"].str.len() > 0
    ]

    df = df[
        ["text", "label"]
    ]

    df.drop_duplicates(
        subset=["text"],
        inplace=True,
    )

    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        PROCESSED_DATA_DIR /
        "cleaned_dataset.csv"
    )

    df.to_csv(
        output_path,
        index=False,
    )

    print(df.head())

    print()

    print("Saved to")

    print(output_path)

    print(f"Final Samples: {len(df)}")


if __name__ == "__main__":
    main()
