from fastapi import APIRouter

from app.api.schemas import HealthResponse
from app.services.model_loader import get_model_status


router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    status = get_model_status()
    all_loaded = (
        status["classifier_loaded"]
        and status["segmenter_loaded"]
    )

    return HealthResponse(
        status="healthy" if all_loaded else "degraded",
        classifier_loaded=status["classifier_loaded"],
        segmenter_loaded=status["segmenter_loaded"],
    )
