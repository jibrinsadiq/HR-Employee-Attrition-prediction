from fastapi import APIRouter, HTTPException, status

from app.api.schemas import EmployeeProfile, PredictionResponse
from app.services.prediction_service import predict_attrition


router = APIRouter(tags=["Classification"])


@router.post("/predict", response_model=PredictionResponse)
def predict(profile: EmployeeProfile) -> PredictionResponse:
    try:
        return predict_attrition(profile)
    except FileNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error
    except (AttributeError, ValueError) as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {error}",
        ) from error
