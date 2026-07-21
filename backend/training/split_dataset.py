import pandas as pd
from sklearn.model_selection import train_test_split

from app.core.config import (
    PROCESSED_DATA_DIR,
    SPLITS_DIR,
    RANDOM_STATE,
)


def main():
    print("Loading cleaned dataset...")

    df = pd.read_csv(
        PROCESSED_DATA_DIR / "cleaned_dataset.csv"
    )

    train_df, temp_df = train_test_split(
        df,
        test_size=0.30,
        stratify=df["label"],
        random_state=RANDOM_STATE,
    )

    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.50,
        stratify=temp_df["label"],
        random_state=RANDOM_STATE,
    )

    SPLITS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    train_df.to_csv(
        SPLITS_DIR / "train.csv",
        index=False,
    )

    val_df.to_csv(
        SPLITS_DIR / "val.csv",
        index=False,
    )

    test_df.to_csv(
        SPLITS_DIR / "test.csv",
        index=False,
    )

    print("\nDataset Split Complete")
    print("-" * 35)
    print(f"Train      : {len(train_df)}")
    print(f"Validation : {len(val_df)}")
    print(f"Test       : {len(test_df)}")
    print(f"Total      : {len(df)}")


if __name__ == "__main__":
    main()
