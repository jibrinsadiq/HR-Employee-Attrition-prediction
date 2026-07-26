# HR Attrition App Scaffold

## What works before models are exported

The FastAPI service launches and `/health` reports `degraded`.
Prediction endpoints return HTTP 503 with the missing artifact path.

## Required model files

Place these fitted, complete scikit-learn pipelines in `artifacts/`:

- `attrition_classifier.joblib`
- `employee_segmenter.joblib`

The classifier must accept raw IBM HR columns.
The segmenter must accept these seven columns:

- YearsAtCompany
- MonthlyIncome
- JobSatisfaction
- EnvironmentSatisfaction
- JobInvolvement
- WorkLifeBalance
- DistanceFromHome

## Local installation

From the repository root:

```powershell
uv add fastapi "uvicorn[standard]" streamlit requests joblib
```

Your existing project should already include pandas, NumPy,
scikit-learn, and XGBoost.

## Launch FastAPI

```powershell
uv run uvicorn app.api.main:app --reload
```

Open:

- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

## Launch Streamlit

Open a second PowerShell terminal:

```powershell
uv run streamlit run app/ui/streamlit_app.py
```

Open:

- http://127.0.0.1:8501

## Docker

After exporting both model files:

```powershell
docker compose up --build
```

Open:

- Streamlit: http://localhost:8501
- FastAPI docs: http://localhost:8000/docs
