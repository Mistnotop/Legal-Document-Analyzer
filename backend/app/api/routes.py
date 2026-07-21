from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.config import settings
from app.models.request_models import TextPredictionRequest
from app.models.response_models import PredictionResponse
from app.services.document_service import extract_text
from app.services.prediction_service import predict

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "healthy"}


@router.get("/version")
async def version():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "model": "LinearSVC + TF-IDF",
    }


@router.post(
    "/predict",
    response_model=PredictionResponse,
)
async def predict_text(request: TextPredictionRequest):
    try:
        return predict(request.text)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post("/predict-document")
async def predict_document(
    file: UploadFile = File(...)
):

    try:

        text = extract_text(file)

        result = predict(text)

        return {
            "filename": file.filename,
            "predicted_class": result["predicted_class"],
            "confidence": result["confidence"],
            "top_predictions": result["top_predictions"],
            "characters": len(text),
            "preview": text[:500],
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
