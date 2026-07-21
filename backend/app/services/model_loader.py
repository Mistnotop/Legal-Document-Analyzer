import joblib

from app.core.config import MODEL_DIR


class ModelLoader:

    _model = None
    _vectorizer = None
    _encoder = None

    @classmethod
    def load(cls):

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
