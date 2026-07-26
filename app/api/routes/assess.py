from fastapi import APIRouter, HTTPException, status

from app.api.schemas import AssessmentResponse, EmployeeProfile
from app.services.prediction_service import predict_attrition
from app.services.segmentation_service import segment_employee


router = APIRouter(tags=["Assessment"])


@router.post("/assess", response_model=AssessmentResponse)
def assess(profile: EmployeeProfile) -> AssessmentResponse:
    try:
        prediction = predict_attrition(profile)
        segment = segment_employee(profile)

        return AssessmentResponse(
            **prediction.model_dump(),
            cluster_id=segment.cluster_id,
            persona=segment.persona,
            suggested_action=segment.suggested_action,
            segment_model_name=segment.model_name,
        )
    except FileNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error
    except (AttributeError, ValueError) as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Assessment failed: {error}",
        ) from error
