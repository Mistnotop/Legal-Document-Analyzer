import joblib
from app.core.config import MODEL_DIR


class ModelLoader:

    _model = None
    _vectorizer = None
    _encoder = None

    @classmethod
    def load(cls):

        print(f"MODEL_DIR = {MODEL_DIR}")
        print(f"best_model exists = {(MODEL_DIR / 'best_model.pkl').exists()}")
        print(f"vectorizer exists = {(MODEL_DIR / 'tfidf_vectorizer.pkl').exists()}")
        print(f"encoder exists = {(MODEL_DIR / 'label_encoder.pkl').exists()}")

        if cls._model is None:

            cls._model = joblib.load(
                MODEL_DIR / "best_model.pkl"
            )

            cls._vectorizer = joblib.load(
                MODEL_DIR / "tfidf_vectorizer.pkl"
            )

            cls._encoder = joblib.load(
                MODEL_DIR / "label_encoder.pkl"
            )

        return (
            cls._model,
            cls._vectorizer,
            cls._encoder,
        )