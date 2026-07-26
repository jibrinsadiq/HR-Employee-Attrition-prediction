import streamlit as st


st.set_page_config(
    page_title="How to use the HR Attrition App",
    page_icon="❓",
    layout="wide",
)

st.title("How to use the HR Attrition App")
st.caption(
    "Follow these steps from loading the data to making an employee prediction."
)

st.page_link(
    "streamlit_app.py",
    label="← Back to assessment",
)

st.header("1. Open the project folder")
st.code(
    r"cd C:\Users\Jibri_rie4meo\Desktop\Trainings\Week4Assignment\HR-Employee-Attrition-prediction",
    language="powershell",
)

st.header("2. Activate the virtual environment")
st.code(r".\.venv\Scripts\Activate.ps1", language="powershell")
st.write("Install the application packages when needed:")
st.code(
    'uv add fastapi "uvicorn[standard]" streamlit requests joblib mlflow',
    language="powershell",
)

st.header("3. Put the dataset in the correct folder")
st.write("The raw IBM HR dataset must be stored at:")
st.code(
    r"data\raw\WA_Fn-UseC_-HR-Employee-Attrition.csv",
    language="text",
)

st.header("4. Clean and prepare the data")
st.code(
    r"uv run python .\scripts\prepare_data.py",
    language="powershell",
)
st.write("The cleaned data is saved at:")
st.code(
    r"data\processed\hr_attrition_cleaned.csv",
    language="text",
)

st.header("5. Train the classification models")
st.write("Train Logistic Regression and Random Forest:")
st.code(
    r"uv run python .\scripts\train_classification.py",
    language="powershell",
)
st.write("Tune and train XGBoost:")
st.code(
    r"uv run python .\scripts\tune_xgboost.py",
    language="powershell",
)

st.header("6. Train and compare the clustering models")
st.code(
    r"uv run python .\scripts\train_clustering.py",
    language="powershell",
)
st.write(
    "This compares K-Means, Agglomerative Clustering, and Gaussian Mixture models."
)

st.header("7. View the latest classification results")
st.code(
    r"uv run python .\scripts\show_mlflow_results.py",
    language="powershell",
)
st.write("The exported comparison files are:")
st.code(
    "reports\\classification_results.csv\n"
    "reports\\classification_results.txt",
    language="text",
)

st.header("8. Export the models used by the live app")
st.write(
    "Run this before starting FastAPI. It creates the trained model files "
    "that the API loads for predictions."
)
st.code(
    r"uv run python .\scripts\export_production_models.py",
    language="powershell",
)
st.write("The command creates:")
st.code(
    "artifacts\\attrition_classifier.joblib\n"
    "artifacts\\employee_segmenter.joblib\n"
    "artifacts\\persona_mapping.json\n"
    "artifacts\\retention_actions.json\n"
    "artifacts\\model_metadata.json",
    language="text",
)

st.header("9. Start FastAPI")
st.code(
    "uv run uvicorn app.api.main:app --reload",
    language="powershell",
)
st.write("Check the API at:")
st.code(
    "Health: http://127.0.0.1:8000/health\n"
    "API documentation: http://127.0.0.1:8000/docs",
    language="text",
)
st.info("Keep this FastAPI terminal running while using Streamlit.")

st.header("10. Start Streamlit")
st.write("Open a second PowerShell terminal in the project folder and run:")
st.code(
    "uv run streamlit run app/ui/streamlit_app.py",
    language="powershell",
)
st.write("Open:")
st.code("http://127.0.0.1:8501", language="text")

st.header("11. Make a prediction")
st.markdown(
    """
1. Enter the employee details on the assessment page.
2. Review the three input tabs.
3. Select **Assess employee**.
4. Streamlit sends the employee profile to FastAPI as JSON.
5. Logistic Regression calculates the attrition risk.
6. K-Means assigns an employee persona.
7. The app displays the risk score, risk band, persona, and retention action.
"""
)

st.header("12. Start everything with Docker")
st.write("First export the `.joblib` models, then run:")
st.code("docker compose up --build", language="powershell")
st.code(
    "Streamlit: http://localhost:8501\n"
    "FastAPI docs: http://localhost:8000/docs\n"
    "Health: http://localhost:8000/health",
    language="text",
)

st.header("Quick start when the models already exist")
terminal_one, terminal_two = st.columns(2)

with terminal_one:
    st.subheader("Terminal 1 — FastAPI")
    st.code(
        "uv run uvicorn app.api.main:app --reload",
        language="powershell",
    )

with terminal_two:
    st.subheader("Terminal 2 — Streamlit")
    st.code(
        "uv run streamlit run app/ui/streamlit_app.py",
        language="powershell",
    )

st.warning(
    "Only load trusted `.joblib` files. This application supports HR review "
    "and must not be used to make automatic employment decisions."
)
