import numpy as np

from app.services.model_loader import ModelLoader
from app.utils.text_cleaner import clean_text


def softmax(values):
    exp = np.exp(values - np.max(values))
    return exp / exp.sum()


def predict(text: str):

    text = clean_text(text)

    if not text:
        raise ValueError("Document text is empty.")

    model, vectorizer, encoder = ModelLoader.load()

    X = vectorizer.transform([text])

    predicted_index = model.predict(X)[0]

    scores = model.decision_function(X)[0]

    probabilities = softmax(scores)

    top_indices = np.argsort(probabilities)[::-1][:3]

    top_predictions = [
        {
            "label": encoder.inverse_transform([i])[0],
            "confidence": round(float(probabilities[i] * 100), 2),
        }
        for i in top_indices
    ]

    return {
        "predicted_class": encoder.inverse_transform([predicted_index])[0],
        "confidence": round(float(probabilities[predicted_index] * 100), 2),
        "top_predictions": top_predictions,
    }
