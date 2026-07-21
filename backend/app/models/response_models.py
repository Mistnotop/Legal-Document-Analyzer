from typing import List

from pydantic import BaseModel


class PredictionItem(BaseModel):
    label: str
    confidence: float


class PredictionResponse(BaseModel):
    predicted_class: str
    confidence: float
    top_predictions: List[PredictionItem]
