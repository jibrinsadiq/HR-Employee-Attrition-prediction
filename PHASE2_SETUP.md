# Phase 2 — Training and Production Model Export

This phase adds reusable training modules and executable scripts.

## Data placement

Place the dataset at:

```text
data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv
```

## Run order

### 1. Prepare a cleaned CSV

```powershell
uv run python .\scripts\prepare_data.py
```

### 2. Train and log Logistic Regression and Random Forest

```powershell
uv run python .\scripts\train_classification.py
```

### 3. Tune and log XGBoost

```powershell
uv run python .\scripts\tune_xgboost.py
```

### 4. Compare clustering approaches

```powershell
uv run python .\scripts\train_clustering.py
```

### 5. Display the latest completed MLflow result for each model

```powershell
uv run python .\scripts\show_mlflow_results.py
```

### 6. Export the production classifier and segmenter

```powershell
uv run python .\scripts\export_production_models.py
```

The export script creates:

```text
artifacts/attrition_classifier.joblib
artifacts/employee_segmenter.joblib
artifacts/persona_mapping.json
artifacts/retention_actions.json
artifacts/model_metadata.json
```

It also derives persona-to-cluster mappings from the newly fitted
K-Means profiles, so cluster IDs do not have to be assumed.

### 7. Launch FastAPI

```powershell
uv run uvicorn app.api.main:app --reload
```

### 8. Launch Streamlit in another terminal

```powershell
uv run streamlit run app/ui/streamlit_app.py
```

## Important design improvement

The production classifier now accepts raw categorical values.
One-hot and ordinal encoding happen inside the saved pipeline.
FastAPI therefore does not recreate dummy columns manually.
