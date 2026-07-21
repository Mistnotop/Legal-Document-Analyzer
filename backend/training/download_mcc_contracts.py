import argparse
import csv
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

import pandas as pd

from app.core.config import ALLOWED_CLASSES, RAW_DATA_DIR


SOURCE_METADATA = RAW_DATA_DIR / "contracts_cleaned_parties_240502.csv"
OUTPUT_METADATA = RAW_DATA_DIR / "downloaded_contracts_metadata.csv"
CONTRACTS_DIR = RAW_DATA_DIR / "contracts"
SEC_BASE_URL = "https://www.sec.gov"


def normalize_url(contract_link: str) -> str:
    return urljoin(SEC_BASE_URL, str(contract_link).strip())


def safe_filename(index: int, contract_link: str) -> str:
    name = Path(str(contract_link).split("?")[0]).name
    if not name:
        name = f"contract_{index}.html"
    if not name.lower().endswith((".html", ".htm", ".txt")):
        name = f"{name}.html"
    return f"{index}_{name}"


def download_file(url: str, destination: Path, timeout: int, user_agent: str) -> bool:
    request = Request(url, headers={"User-Agent": user_agent})

    try:
        with urlopen(request, timeout=timeout) as response:
            destination.write_bytes(response.read())
        return True
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        print(f"Failed: {url} ({exc})")
        return False


def validate_labels(metadata_path: Path, label_column: str, required_classes: set[str]) -> None:
    labels = set()

    for chunk in pd.read_csv(
        metadata_path,
        usecols=[label_column],
        chunksize=100000,
        low_memory=False,
    ):
        labels.update(chunk[label_column].dropna().astype(str).str.strip())

    missing = sorted(required_classes - labels)
    present = sorted(required_classes & labels)

    print(f"Label column: {label_column}")
    print(f"Required classes found: {present}")

    if missing:
        print(f"Required classes missing: {missing}")
        print("Available labels:")
        for label in sorted(labels):
            print(f"- {label}")
        raise SystemExit(
            "Stopping because the required classes are not present exactly in the metadata."
        )


def iter_selected_rows(metadata_path: Path, label_column: str):
    usecols = [
        "year",
        "cik",
        "company.name",
        "date.filed",
        "contract.link",
        "contract",
        "description",
        "agreement_type",
        "type_label",
    ]

    for chunk in pd.read_csv(metadata_path, usecols=usecols, chunksize=50000, low_memory=False):
        for index, row in chunk.iterrows():
            category = str(row.get(label_column, "")).strip()

            if category not in ALLOWED_CLASSES:
                continue

            contract_link = row.get("contract.link") or row.get("contract")
            if pd.isna(contract_link) or not str(contract_link).strip():
                continue

            yield index, row, category


def main():
    parser = argparse.ArgumentParser(
        description="Download a capped MCC contract subset for NyaySetu training."
    )
    parser.add_argument("--metadata", type=Path, default=SOURCE_METADATA)
    parser.add_argument("--limit-per-class", type=int, default=500)
    parser.add_argument("--output-metadata", type=Path, default=OUTPUT_METADATA)
    parser.add_argument("--contracts-dir", type=Path, default=CONTRACTS_DIR)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--delay", type=float, default=0.1)
    parser.add_argument("--label-column", default="agreement_type")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--user-agent",
        default="NyaySetu legal document analyzer contact@example.com",
        help="SEC requests require a descriptive user agent. Replace with your email.",
    )
    args = parser.parse_args()

    args.contracts_dir.mkdir(parents=True, exist_ok=True)
    args.output_metadata.parent.mkdir(parents=True, exist_ok=True)
    validate_labels(args.metadata, args.label_column, set(ALLOWED_CLASSES))

    fieldnames = [
        "label",
        "local_path",
        "source_url",
        "description",
        "agreement_type",
        "type_label",
        "year",
        "cik",
        "company.name",
        "date.filed",
    ]

    rows_written = 0
    counts = {category: 0 for category in ALLOWED_CLASSES}

    with args.output_metadata.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for index, row, label in iter_selected_rows(
            args.metadata,
            args.label_column,
        ):
            if counts[label] >= args.limit_per_class:
                continue

            if all(count >= args.limit_per_class for count in counts.values()):
                break

            contract_link = row.get("contract.link") or row.get("contract")
            source_url = normalize_url(contract_link)
            destination = args.contracts_dir / label / safe_filename(index, contract_link)
            destination.parent.mkdir(parents=True, exist_ok=True)

            if args.dry_run:
                downloaded = True
            elif destination.exists() and not args.overwrite:
                downloaded = True
            else:
                downloaded = download_file(
                    source_url,
                    destination,
                    args.timeout,
                    args.user_agent,
                )
                time.sleep(args.delay)

            if not downloaded:
                continue

            counts[label] += 1
            writer.writerow(
                {
                    "label": label,
                    "local_path": str(destination.relative_to(RAW_DATA_DIR)),
                    "source_url": source_url,
                    "description": row.get("description", ""),
                    "agreement_type": row.get("agreement_type", ""),
                    "type_label": row.get("type_label", ""),
                    "year": row.get("year", ""),
                    "cik": row.get("cik", ""),
                    "company.name": row.get("company.name", ""),
                    "date.filed": row.get("date.filed", ""),
                }
            )
            rows_written += 1

            if rows_written % 100 == 0:
                print(f"Downloaded metadata rows: {rows_written} | {counts}")

    print("Done")
    print(f"Metadata: {args.output_metadata}")
    print(f"Contracts: {args.contracts_dir}")
    print(f"Rows written: {rows_written}")
    print(counts)


if __name__ == "__main__":
    main()
