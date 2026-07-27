import os

import requests
import streamlit as st


API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000",
).rstrip("/")


def risk_class(band: str) -> str:
    """Map an API risk-band string to a CSS modifier class."""
    band_lower = (band or "").lower()
    if "high" in band_lower:
        return "risk-high"
    if "med" in band_lower:
        return "risk-medium"
    return "risk-low"


st.set_page_config(
    page_title="HR Attrition Intelligence",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Sans:wght@600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background-color: #F6F7F9;
        }

        .block-container {
            max-width: 1550px;
            padding-top: 1.1rem;
            padding-bottom: 1rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
        }

        /* Custom header (replaces st.title/st.caption) */
        .app-header {
            padding-bottom: 0.9rem;
            margin-bottom: 1.1rem;
            border-bottom: 1px solid #E3E7ED;
        }
        .app-header-title {
            font-family: 'IBM Plex Sans', sans-serif;
            font-size: 1.7rem;
            font-weight: 700;
            color: #1B2430;
            letter-spacing: -0.01em;
        }
        .app-header-caption {
            font-size: 0.92rem;
            color: #5D6B82;
            margin-top: 0.25rem;
        }

        h2, h3 {
            font-family: 'IBM Plex Sans', sans-serif;
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            color: #1B2430;
            margin-top: 0.3rem !important;
            margin-bottom: 0.5rem !important;
        }

        [data-testid="stCaptionContainer"] {
            color: #5D6B82;
            margin-bottom: 0.3rem;
        }

        [data-testid="stVerticalBlock"] {
            gap: 0.4rem;
        }

        [data-testid="stHorizontalBlock"] {
            gap: 0.6rem;
        }

        [data-testid="stWidgetLabel"] p {
            font-size: 0.8rem;
            font-weight: 500;
            color: #3D4A5E;
            margin-bottom: 0.1rem;
        }

        div[data-baseweb="select"] > div,
        div[data-testid="stNumberInput"] input {
            min-height: 2.1rem;
            height: 2.1rem;
            font-size: 0.85rem;
            border-radius: 0.4rem;
            border-color: #D7DCE3 !important;
        }

        div[data-testid="stSlider"] {
            padding-top: 0.15rem;
            padding-bottom: 0.15rem;
        }

        /* Form as a card */
        div[data-testid="stForm"] {
            background: #FFFFFF;
            border: 1px solid #E3E7ED;
            border-radius: 0.75rem;
            padding: 1.1rem 1.2rem 0.9rem 1.2rem;
            box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
        }

        button[data-baseweb="tab"] {
            height: 2.2rem;
            padding-top: 0.25rem;
            padding-bottom: 0.25rem;
            font-weight: 600;
            font-size: 0.85rem;
        }

        [data-testid="stFormSubmitButton"] > button {
            height: 2.4rem;
            font-weight: 600;
            border-radius: 0.5rem;
            background-color: #2E5077;
            color: #FFFFFF;
            border: none;
            margin-top: 0.6rem;
        }
        [data-testid="stFormSubmitButton"] > button:hover {
            background-color: #24405F;
            color: #FFFFFF;
        }

        div[data-testid="stMetric"] {
            padding: 0.6rem 0.7rem;
            background: #FFFFFF;
            border: 1px solid #E3E7ED;
            border-radius: 0.6rem;
        }

        div[data-testid="stMetricLabel"] {
            font-size: 0.74rem;
            color: #5D6B82;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.02em;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.3rem;
            font-weight: 700;
            color: #1B2430;
        }

        .result-card {
            background: #FFFFFF;
            padding: 0.9rem 1rem;
            border: 1px solid #E3E7ED;
            border-left: 4px solid #2E5077;
            border-radius: 0.5rem;
            margin-bottom: 0.55rem;
            box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
        }
        .result-card.risk-high { border-left-color: #DC2626; }
        .result-card.risk-medium { border-left-color: #D97706; }
        .result-card.risk-low { border-left-color: #16A34A; }

        .result-heading {
            font-size: 0.72rem;
            font-weight: 600;
            color: #5D6B82;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 0.3rem;
        }

        .result-value {
            font-size: 1.05rem;
            font-weight: 700;
            color: #1B2430;
            margin-bottom: 0.15rem;
        }

        .risk-score-value {
            font-size: 1.9rem;
            font-weight: 700;
            color: #1B2430;
            line-height: 1.1;
            margin-bottom: 0.4rem;
        }

        .risk-badge {
            display: inline-block;
            padding: 0.22rem 0.7rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .risk-badge.risk-high { background: #FEE2E2; color: #B91C1C; }
        .risk-badge.risk-medium { background: #FEF3C7; color: #B45309; }
        .risk-badge.risk-low { background: #DCFCE7; color: #15803D; }

        .small-note {
            font-size: 0.72rem;
            color: #7C8698;
            margin-top: 0.6rem;
        }

        footer { visibility: hidden; }
        #MainMenu { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="app-header">
        <div class="app-header-title">HR Attrition Risk &amp; Persona Assessment</div>
        <div class="app-header-caption">
            Enter an employee profile to generate an attrition risk score,
            employee persona, and suggested retention action.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("❓ Help / How to use", expanded=False):
    help_tab1, help_tab2, help_tab3 = st.tabs(
        [
            "Prepare models",
            "Run the app",
            "Make a prediction",
        ]
    )

    with help_tab1:
        st.markdown("**1. Put the dataset here:**")
        st.code(
            r"data\raw\WA_Fn-UseC_-HR-Employee-Attrition.csv",
            language="text",
        )

        st.markdown("**2. Prepare the cleaned data:**")
        st.code(
            r"uv run python .\scripts\prepare_data.py",
            language="powershell",
        )

        st.markdown(
            "**3. Train Logistic Regression and Random Forest:**"
        )
        st.code(
            r"uv run python .\scripts\train_classification.py",
            language="powershell",
        )

        st.markdown("**4. Tune XGBoost:**")
        st.code(
            r"uv run python .\scripts\tune_xgboost.py",
            language="powershell",
        )

        st.markdown("**5. Compare clustering models:**")
        st.code(
            r"uv run python .\scripts\train_clustering.py",
            language="powershell",
        )

        st.markdown("**6. Export the production models:**")
        st.code(
            r"uv run python .\scripts\export_production_models.py",
            language="powershell",
        )

        st.caption(
            "This creates the classifier and segmenter .joblib files "
            "inside the artifacts folder."
        )

    with help_tab2:
        st.markdown("**Terminal 1 — start FastAPI:**")
        st.code(
            r"uv run uvicorn app.api.main:app --reload",
            language="powershell",
        )

        st.markdown("**Terminal 2 — start Streamlit:**")
        st.code(
            r"uv run streamlit run app/ui/streamlit_app.py",
            language="powershell",
        )

        st.markdown("**Useful addresses:**")
        st.code(
            """Streamlit: http://127.0.0.1:8501
FastAPI docs: http://127.0.0.1:8000/docs
Health check: http://127.0.0.1:8000/health""",
            language="text",
        )

        st.markdown("**Docker option:**")
        st.code(
            "docker compose up --build",
            language="powershell",
        )

    with help_tab3:
        st.markdown(
            """
            1. Enter the employee information across the three tabs.
            2. Select **Assess employee**.
            3. Streamlit sends the profile to `POST /assess`.
            4. FastAPI calculates the attrition risk and persona.
            5. The result appears on the right side of the page.
            """
        )

        st.info(
            "FastAPI must be running before the assessment can work."
        )



if "assessment_result" not in st.session_state:
    st.session_state.assessment_result = None

if "assessment_error" not in st.session_state:
    st.session_state.assessment_error = None


form_column, result_column = st.columns([2.4, 1], gap="medium")


with form_column:
    with st.form("employee_profile"):
        role_tab, engagement_tab, additional_tab = st.tabs(
            [
                "Personal, role & pay",
                "Satisfaction & career",
                "Additional inputs",
            ]
        )

        with role_tab:
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                age = st.number_input(
                    "Age",
                    min_value=18,
                    max_value=100,
                    value=35,
                )
                gender = st.selectbox(
                    "Gender",
                    ["Female", "Male"],
                )
                marital_status = st.selectbox(
                    "Marital status",
                    ["Married", "Single", "Divorced"],
                )

            with col2:
                department = st.selectbox(
                    "Department",
                    [
                        "Research & Development",
                        "Sales",
                        "Human Resources",
                    ],
                )
                job_role = st.selectbox(
                    "Job role",
                    [
                        "Research Scientist",
                        "Laboratory Technician",
                        "Sales Executive",
                        "Manufacturing Director",
                        "Healthcare Representative",
                        "Manager",
                        "Sales Representative",
                        "Research Director",
                        "Human Resources",
                    ],
                )
                job_level = st.slider(
                    "Job level",
                    min_value=1,
                    max_value=5,
                    value=2,
                )

            with col3:
                monthly_income = st.number_input(
                    "Monthly income",
                    min_value=0.0,
                    value=6500.0,
                    step=100.0,
                )
                monthly_rate = st.number_input(
                    "Monthly rate",
                    min_value=0.0,
                    value=14000.0,
                )
                hourly_rate = st.number_input(
                    "Hourly rate",
                    min_value=0.0,
                    value=65.0,
                )

            with col4:
                business_travel = st.selectbox(
                    "Business travel",
                    [
                        "Travel_Rarely",
                        "Non-Travel",
                        "Travel_Frequently",
                    ],
                )
                over_time = st.selectbox(
                    "Overtime",
                    ["No", "Yes"],
                )
                distance_from_home = st.number_input(
                    "Distance from home",
                    min_value=0.0,
                    value=9.0,
                )

        with engagement_tab:
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                job_satisfaction = st.slider(
                    "Job satisfaction",
                    min_value=1,
                    max_value=4,
                    value=3,
                )
                environment_satisfaction = st.slider(
                    "Environment satisfaction",
                    min_value=1,
                    max_value=4,
                    value=3,
                )
                relationship_satisfaction = st.slider(
                    "Relationship satisfaction",
                    min_value=1,
                    max_value=4,
                    value=3,
                )

            with col2:
                job_involvement = st.slider(
                    "Job involvement",
                    min_value=1,
                    max_value=4,
                    value=3,
                )
                work_life_balance = st.slider(
                    "Work-life balance",
                    min_value=1,
                    max_value=4,
                    value=3,
                )
                performance_rating = st.slider(
                    "Performance rating",
                    min_value=1,
                    max_value=4,
                    value=3,
                )

            with col3:
                total_working_years = st.number_input(
                    "Total working years",
                    min_value=0,
                    value=10,
                )
                years_at_company = st.number_input(
                    "Years at company",
                    min_value=0,
                    value=7,
                )
                years_in_current_role = st.number_input(
                    "Years in current role",
                    min_value=0,
                    value=4,
                )

            with col4:
                years_since_last_promotion = st.number_input(
                    "Years since last promotion",
                    min_value=0,
                    value=2,
                )
                years_with_current_manager = st.number_input(
                    "Years with current manager",
                    min_value=0,
                    value=4,
                )
                training_times_last_year = st.number_input(
                    "Training sessions last year",
                    min_value=0,
                    value=3,
                )

        with additional_tab:
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                education = st.slider(
                    "Education level",
                    min_value=1,
                    max_value=5,
                    value=3,
                )
                education_field = st.selectbox(
                    "Education field",
                    [
                        "Life Sciences",
                        "Medical",
                        "Marketing",
                        "Technical Degree",
                        "Other",
                        "Human Resources",
                    ],
                )

            with col2:
                daily_rate = st.number_input(
                    "Daily rate",
                    min_value=0.0,
                    value=800.0,
                )
                percent_salary_hike = st.number_input(
                    "Percent salary hike",
                    min_value=0.0,
                    value=14.0,
                )

            with col3:
                num_companies_worked = st.number_input(
                    "Number of companies worked",
                    min_value=0,
                    value=2,
                )
                stock_option_level = st.slider(
                    "Stock option level",
                    min_value=0,
                    max_value=3,
                    value=1,
                )

            with col4:
                st.info(
                    "All original model inputs are retained. "
                    "Use the tabs to keep the page compact."
                )

        submitted = st.form_submit_button(
            "Assess employee",
            use_container_width=True,
        )

    if submitted:
        payload = {
            "age": age,
            "business_travel": business_travel,
            "daily_rate": daily_rate,
            "department": department,
            "distance_from_home": distance_from_home,
            "education": education,
            "education_field": education_field,
            "environment_satisfaction": environment_satisfaction,
            "gender": gender,
            "hourly_rate": hourly_rate,
            "job_involvement": job_involvement,
            "job_level": job_level,
            "job_role": job_role,
            "job_satisfaction": job_satisfaction,
            "marital_status": marital_status,
            "monthly_income": monthly_income,
            "monthly_rate": monthly_rate,
            "num_companies_worked": num_companies_worked,
            "over_time": over_time,
            "percent_salary_hike": percent_salary_hike,
            "performance_rating": performance_rating,
            "relationship_satisfaction": relationship_satisfaction,
            "stock_option_level": stock_option_level,
            "total_working_years": total_working_years,
            "training_times_last_year": training_times_last_year,
            "work_life_balance": work_life_balance,
            "years_at_company": years_at_company,
            "years_in_current_role": years_in_current_role,
            "years_since_last_promotion": years_since_last_promotion,
            "years_with_current_manager": years_with_current_manager,
        }

        try:
            response = requests.post(
                f"{API_BASE_URL}/assess",
                json=payload,
                timeout=20,
            )
            response.raise_for_status()
            st.session_state.assessment_result = response.json()
            st.session_state.assessment_error = None

        except requests.HTTPError as error:
            detail = "Unknown API error"

            try:
                detail = error.response.json().get(
                    "detail",
                    detail,
                )
            except ValueError:
                pass

            st.session_state.assessment_result = None
            st.session_state.assessment_error = (
                f"Assessment failed: {detail}"
            )

        except requests.RequestException as error:
            st.session_state.assessment_result = None
            st.session_state.assessment_error = (
                "Unable to contact the FastAPI service. "
                f"API URL: {API_BASE_URL}. Error: {error}"
            )


with result_column:
    st.subheader("Assessment result")

    if st.session_state.assessment_error:
        st.error(st.session_state.assessment_error)

    result = st.session_state.assessment_result

    if result:
        band = result["risk_band"]
        css_class = risk_class(band)

        prediction_text = (
            "At risk" if result["prediction"] == 1 else "Lower risk"
        )

        st.markdown(
            f"""
            <div class="result-card {css_class}">
                <div class="result-heading">Attrition risk score</div>
                <div class="risk-score-value">{result['risk_score'] * 100:.1f}%</div>
                <span class="risk-badge {css_class}">{band}</span>
                <span style="margin-left:0.5rem; font-size:0.8rem; color:#5D6B82;">
                    {prediction_text}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.progress(
            min(
                max(float(result["risk_score"]), 0.0),
                1.0,
            )
        )

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-heading">Employee persona</div>
                <div class="result-value">{result["persona"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-heading">
                    Suggested retention action
                </div>
                <div>{result["suggested_action"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander("Model information"):
            st.write(
                {
                    "classification_model":
                        result["model_name"],
                    "classification_version":
                        result["model_version"],
                    "decision_threshold":
                        result["decision_threshold"],
                    "segmentation_model":
                        result["segment_model_name"],
                    "cluster_id":
                        result["cluster_id"],
                }
            )

    else:
        st.info(
            "Complete the employee profile and select "
            "Assess employee."
        )

    st.markdown(
        """
        <div class="small-note">
            This tool supports HR review and does not make
            employment decisions. Predictions reflect patterns in
            the training dataset and may not represent every
            employee's circumstances.
        </div>
        """,
        unsafe_allow_html=True,
    )
