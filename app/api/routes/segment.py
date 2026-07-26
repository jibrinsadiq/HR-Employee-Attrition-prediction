from fastapi import APIRouter, HTTPException, Query, status
import pandas as pd

from app.api.schemas import SegmentResponse
from app.services.model_loader import (
    get_model_metadata,
    get_segmenter,
)
from app.services.retention_service import get_persona_and_action


router = APIRouter(tags=["Segmentation"])


@router.get("/segment", response_model=SegmentResponse)
def segment(
    years_at_company: int = Query(ge=0),
    monthly_income: float = Query(ge=0),
    job_satisfaction: int = Query(ge=1, le=4),
    environment_satisfaction: int = Query(ge=1, le=4),
    job_involvement: int = Query(ge=1, le=4),
    work_life_balance: int = Query(ge=1, le=4),
    distance_from_home: float = Query(ge=0),
) -> SegmentResponse:
    try:
        model_input = pd.DataFrame(
            [
                {
                    "YearsAtCompany": years_at_company,
                    "MonthlyIncome": monthly_income,
                    "JobSatisfaction": job_satisfaction,
                    "EnvironmentSatisfaction":
                        environment_satisfaction,
                    "JobInvolvement": job_involvement,
                    "WorkLifeBalance": work_life_balance,
                    "DistanceFromHome": distance_from_home,
                }
            ]
        )

        model = get_segmenter()
        cluster_id = int(model.predict(model_input)[0])
        persona, action = get_persona_and_action(cluster_id)
        metadata = get_model_metadata()

        return SegmentResponse(
            cluster_id=cluster_id,
            persona=persona,
            suggested_action=action,
            model_name=str(
                metadata.get("segmenter_name", "KMeans")
            ),
        )
    except FileNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error
    except (AttributeError, ValueError) as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Segmentation failed: {error}",
        ) from error
