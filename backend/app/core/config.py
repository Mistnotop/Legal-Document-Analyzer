from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Legal Document Analyzer API"
    app_version: str = "1.0.0"
    app_description: str = (
        "AI-powered Legal Document Classification using the Stanford MCC Dataset"
    )
    cors_origins: str = "http://127.0.0.1:5173,http://localhost:5173"

    @property
    def cors_origin_list(self):
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]

    class Config:
        env_file = ".env"


settings = Settings()

# Project Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATASET_DIR = BASE_DIR / "dataset"
RAW_DATA_DIR = DATASET_DIR / "raw"
PROCESSED_DATA_DIR = DATASET_DIR / "processed"
SPLITS_DIR = DATASET_DIR / "splits"

UPLOAD_DIR = BASE_DIR / "app" / "uploads"
MODEL_DIR = BASE_DIR / "app" / "saved_models"
MAX_UPLOAD_SIZE_BYTES = 10 * 1024 * 1024
ALLOWED_UPLOAD_EXTENSIONS = {".pdf", ".docx", ".txt"}

# Allowed Contract Categories
ALLOWED_CLASSES = [
    "employment",
    "security",
    "purchase&ma",
    "services&supply",
    "shareholder",
    "other",
    "lease",
    "na",
]

# ML Configuration
MAX_FEATURES = 50000
NGRAM_RANGE = (1, 2)
MIN_DF = 2
MAX_DF = 0.95
SUBLINEAR_TF = True

SVM_C = 2.0
RANDOM_STATE = 42
