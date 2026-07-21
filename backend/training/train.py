import time

import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC

from app.core.config import (
    SPLITS_DIR,
    MODEL_DIR,
    MAX_FEATURES,
    NGRAM_RANGE,
    MIN_DF,
    MAX_DF,
    SUBLINEAR_TF,
    SVM_C,
    RANDOM_STATE,
)


def main():

    print("=" * 60)
    print("LEGAL DOCUMENT ANALYZER - MODEL TRAINING")
    print("=" * 60)

    start_time = time.time()

    print("\nLoading training dataset...")

    train_df = pd.read_csv(
        SPLITS_DIR / "train.csv"
    )

    print(f"Training samples : {len(train_df)}")

    print("\nEncoding labels...")

    label_encoder = LabelEncoder()

    y_train = label_encoder.fit_transform(
        train_df["label"]
    )

    print(f"Classes : {list(label_encoder.classes_)}")

    print("\nBuilding TF-IDF Vectorizer...")

    vectorizer = TfidfVectorizer(
        max_features=MAX_FEATURES,
        ngram_range=NGRAM_RANGE,
        min_df=MIN_DF,
        max_df=MAX_DF,
        sublinear_tf=SUBLINEAR_TF,
    )

    X_train = vectorizer.fit_transform(
        train_df["text"]
    )

    print(f"Vocabulary Size : {len(vectorizer.vocabulary_):,}")

    print("\nTraining Linear SVM...")

    model = LinearSVC(
        C=SVM_C,
        random_state=RANDOM_STATE,
    )

    model.fit(
        X_train,
        y_train,
    )

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("\nSaving model artifacts...")

    joblib.dump(
        model,
        MODEL_DIR / "best_model.pkl",
    )

    joblib.dump(
        vectorizer,
        MODEL_DIR / "tfidf_vectorizer.pkl",
    )

    joblib.dump(
        label_encoder,
        MODEL_DIR / "label_encoder.pkl",
    )

    elapsed = time.time() - start_time

    print("\nTraining Complete")
    print("-" * 40)
    print(f"Training Time : {elapsed:.2f} sec")
    print(f"Model Folder  : {MODEL_DIR}")
    print("Saved Files:")
    print("  best_model.pkl")
    print("  tfidf_vectorizer.pkl")
    print("  label_encoder.pkl")
    print("=" * 60)


if __name__ == "__main__":
    main()
