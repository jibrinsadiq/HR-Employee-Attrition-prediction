from fastapi import FastAPI

from app.api.routes.assess import router as assess_router
from app.api.routes.health import router as health_router
from app.api.routes.predict import router as predict_router
from app.api.routes.segment import router as segment_router


app = FastAPI(
    title="HR Attrition Intelligence API",
    description=(
        "Attrition risk scoring and employee persona segmentation. "
        "Outputs support HR review and must not be used as automatic "
        "employment decisions."
    ),
    version="1.0.0",
)

app.include_router(health_router)
app.include_router(predict_router)
app.include_router(segment_router)
app.include_router(assess_router)


@app.get("/", tags=["Root"])
def root() -> dict[str, str]:
    return {
        "message": "HR Attrition Intelligence API",
        "docs": "/docs",
        "health": "/health",
    }
