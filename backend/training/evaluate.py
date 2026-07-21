import json

import joblib
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)

from app.core.config import (
    SPLITS_DIR,
    MODEL_DIR,
)


def evaluate_dataset(name, dataframe, model, vectorizer, encoder):
    X = vectorizer.transform(dataframe["text"])
    y_true = encoder.transform(dataframe["label"])
    y_pred = model.predict(X)

    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "macro_precision": precision_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0,
        ),
        "macro_recall": recall_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0,
        ),
        "macro_f1": f1_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0,
        ),
        "weighted_f1": f1_score(
            y_true,
            y_pred,
            average="weighted",
            zero_division=0,
        ),
    }

    print(f"\n{name.upper()} RESULTS")
    print("=" * 60)

    for key, value in metrics.items():
        print(f"{key:20}: {value:.4f}")

    print("\nClassification Report\n")

    report = classification_report(
        y_true,
        y_pred,
        target_names=encoder.classes_,
        zero_division=0,
    )

    print(report)

    cm = confusion_matrix(y_true, y_pred)

    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=encoder.classes_,
    )

    fig, ax = plt.subplots(figsize=(10, 8))

    disp.plot(
        ax=ax,
        xticks_rotation=45,
        colorbar=False,
    )

    plt.tight_layout()

    output = MODEL_DIR / f"{name.lower()}_confusion_matrix.png"

    plt.savefig(output, dpi=300)

    plt.close()

    return metrics, report


def main():

    model = joblib.load(
        MODEL_DIR / "best_model.pkl"
    )

    vectorizer = joblib.load(
        MODEL_DIR / "tfidf_vectorizer.pkl"
    )

    encoder = joblib.load(
        MODEL_DIR / "label_encoder.pkl"
    )

    val_df = pd.read_csv(
        SPLITS_DIR / "val.csv"
    )

    test_df = pd.read_csv(
        SPLITS_DIR / "test.csv"
    )

    val_metrics, val_report = evaluate_dataset(
        "Validation",
        val_df,
        model,
        vectorizer,
        encoder,
    )

    test_metrics, test_report = evaluate_dataset(
        "Test",
        test_df,
        model,
        vectorizer,
        encoder,
    )

    metrics = {
        "validation": val_metrics,
        "test": test_metrics,
    }

    with open(
        MODEL_DIR / "metrics.json",
        "w",
    ) as f:
        json.dump(metrics, f, indent=4)

    with open(
        MODEL_DIR / "classification_report.txt",
        "w",
        encoding="utf-8",
    ) as f:

        f.write("VALIDATION\n\n")
        f.write(val_report)

        f.write("\n\nTEST\n\n")
        f.write(test_report)

    print("\nSaved")

    print("metrics.json")
    print("classification_report.txt")
    print("validation_confusion_matrix.png")
    print("test_confusion_matrix.png")


if __name__ == "__main__":
    main()
