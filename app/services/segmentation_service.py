import pandas as pd

from app.api.schemas import EmployeeProfile, SegmentResponse
from app.services.model_loader import (
    get_model_metadata,
    get_segmenter,
)
from app.services.retention_service import get_persona_and_action


def segment_employee(
    profile: EmployeeProfile,
) -> SegmentResponse:
    model = get_segmenter()
    metadata = get_model_metadata()

    model_input = pd.DataFrame([profile.to_segment_dict()])
    cluster_id = int(model.predict(model_input)[0])

    persona, action = get_persona_and_action(cluster_id)

    return SegmentResponse(
        cluster_id=cluster_id,
        persona=persona,
        suggested_action=action,
        model_name=str(
            metadata.get("segmenter_name", "KMeans")
        ),
    )
