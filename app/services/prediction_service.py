import pandas as pd

from app.api.schemas import EmployeeProfile, PredictionResponse
from app.services.model_loader import (
    get_classifier,
    get_model_metadata,
)


def _risk_band(score: float) -> str:
    if score < 0.35:
        return "Low"
    if score < 0.60:
        return "Medium"
    return "High"


def predict_attrition(
    profile: EmployeeProfile,
) -> PredictionResponse:
    model = get_classifier()
    metadata = get_model_metadata()

    model_input = pd.DataFrame([profile.to_model_dict()])
    risk_score = float(model.predict_proba(model_input)[0, 1])

    threshold = float(
        metadata.get("classification_threshold", 0.50)
    )
    prediction = int(risk_score >= threshold)

    return PredictionResponse(
        prediction=prediction,
        risk_score=round(risk_score, 4),
        risk_band=_risk_band(risk_score),
        decision_threshold=threshold,
        model_name=str(
            metadata.get(
                "classifier_name",
                "LogisticRegression",
            )
        ),
        model_version=str(
            metadata.get(
                "classifier_version",
                "unversioned",
            )
        ),
    )
