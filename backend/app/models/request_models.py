from pydantic import BaseModel


class TextPredictionRequest(BaseModel):
    text: str


class DocumentResponse(BaseModel):
    filename: str
    extracted_text: str
