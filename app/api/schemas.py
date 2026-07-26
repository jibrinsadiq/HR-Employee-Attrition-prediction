from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class EmployeeProfile(BaseModel):
    """Raw employee profile accepted by the classification API."""

    model_config = ConfigDict(extra="forbid")

    age: int = Field(ge=18, le=100)
    business_travel: Literal[
        "Non-Travel",
        "Travel_Rarely",
        "Travel_Frequently",
    ]
    daily_rate: float = Field(ge=0)
    department: Literal[
        "Human Resources",
        "Research & Development",
        "Sales",
    ]
    distance_from_home: float = Field(ge=0)
    education: int = Field(ge=1, le=5)
    education_field: Literal[
        "Human Resources",
        "Life Sciences",
        "Marketing",
        "Medical",
        "Other",
        "Technical Degree",
    ]
    environment_satisfaction: int = Field(ge=1, le=4)
    gender: Literal["Female", "Male"]
    hourly_rate: float = Field(ge=0)
    job_involvement: int = Field(ge=1, le=4)
    job_level: int = Field(ge=1, le=5)
    job_role: Literal[
        "Healthcare Representative",
        "Human Resources",
        "Laboratory Technician",
        "Manager",
        "Manufacturing Director",
        "Research Director",
        "Research Scientist",
        "Sales Executive",
        "Sales Representative",
    ]
    job_satisfaction: int = Field(ge=1, le=4)
    marital_status: Literal["Divorced", "Married", "Single"]
    monthly_income: float = Field(ge=0)
    monthly_rate: float = Field(ge=0)
    num_companies_worked: int = Field(ge=0)
    over_time: Literal["No", "Yes"]
    percent_salary_hike: float = Field(ge=0)
    performance_rating: int = Field(ge=1, le=4)
    relationship_satisfaction: int = Field(ge=1, le=4)
    stock_option_level: int = Field(ge=0, le=3)
    total_working_years: int = Field(ge=0)
    training_times_last_year: int = Field(ge=0)
    work_life_balance: int = Field(ge=1, le=4)
    years_at_company: int = Field(ge=0)
    years_in_current_role: int = Field(ge=0)
    years_since_last_promotion: int = Field(ge=0)
    years_with_current_manager: int = Field(ge=0)

    def to_model_dict(self) -> dict[str, object]:
        """Return column names matching the original IBM HR dataset."""
        return {
            "Age": self.age,
            "BusinessTravel": self.business_travel,
            "DailyRate": self.daily_rate,
            "Department": self.department,
            "DistanceFromHome": self.distance_from_home,
            "Education": self.education,
            "EducationField": self.education_field,
            "EnvironmentSatisfaction": self.environment_satisfaction,
            "Gender": self.gender,
            "HourlyRate": self.hourly_rate,
            "JobInvolvement": self.job_involvement,
            "JobLevel": self.job_level,
            "JobRole": self.job_role,
            "JobSatisfaction": self.job_satisfaction,
            "MaritalStatus": self.marital_status,
            "MonthlyIncome": self.monthly_income,
            "MonthlyRate": self.monthly_rate,
            "NumCompaniesWorked": self.num_companies_worked,
            "OverTime": self.over_time,
            "PercentSalaryHike": self.percent_salary_hike,
            "PerformanceRating": self.performance_rating,
            "RelationshipSatisfaction": self.relationship_satisfaction,
            "StockOptionLevel": self.stock_option_level,
            "TotalWorkingYears": self.total_working_years,
            "TrainingTimesLastYear": self.training_times_last_year,
            "WorkLifeBalance": self.work_life_balance,
            "YearsAtCompany": self.years_at_company,
            "YearsInCurrentRole": self.years_in_current_role,
            "YearsSinceLastPromotion": self.years_since_last_promotion,
            "YearsWithCurrManager": self.years_with_current_manager,
        }

    def to_segment_dict(self) -> dict[str, float | int]:
        """Return the seven fields used by the selected K-Means segmenter."""
        return {
            "YearsAtCompany": self.years_at_company,
            "MonthlyIncome": self.monthly_income,
            "JobSatisfaction": self.job_satisfaction,
            "EnvironmentSatisfaction": self.environment_satisfaction,
            "JobInvolvement": self.job_involvement,
            "WorkLifeBalance": self.work_life_balance,
            "DistanceFromHome": self.distance_from_home,
        }


class PredictionResponse(BaseModel):
    prediction: int
    risk_score: float
    risk_band: Literal["Low", "Medium", "High"]
    decision_threshold: float
    model_name: str
    model_version: str


class SegmentResponse(BaseModel):
    cluster_id: int
    persona: str
    suggested_action: str
    model_name: str


class AssessmentResponse(PredictionResponse):
    cluster_id: int
    persona: str
    suggested_action: str
    segment_model_name: str


class HealthResponse(BaseModel):
    status: Literal["healthy", "degraded"]
    classifier_loaded: bool
    segmenter_loaded: bool
