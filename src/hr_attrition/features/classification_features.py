CLASSIFICATION_TARGET = "Attrition_encoded"

SKEWED_NUMERIC_FEATURES = [
    "MonthlyIncome",
    "NumCompaniesWorked",
    "TotalWorkingYears",
    "YearsAtCompany",
    "YearsSinceLastPromotion",
]

NUMERIC_FEATURES = [
    "Age",
    "DailyRate",
    "DistanceFromHome",
    "Education",
    "EnvironmentSatisfaction",
    "HourlyRate",
    "JobInvolvement",
    "JobLevel",
    "JobSatisfaction",
    "MonthlyRate",
    "PercentSalaryHike",
    "PerformanceRating",
    "RelationshipSatisfaction",
    "StockOptionLevel",
    "TrainingTimesLastYear",
    "WorkLifeBalance",
    "YearsInCurrentRole",
    "YearsWithCurrManager",
]

ORDINAL_FEATURES = [
    "BusinessTravel",
]

BINARY_CATEGORICAL_FEATURES = [
    "Gender",
    "OverTime",
]

NOMINAL_CATEGORICAL_FEATURES = [
    "MaritalStatus",
    "JobRole",
    "Department",
    "EducationField",
]

CLASSIFICATION_FEATURES = (
    SKEWED_NUMERIC_FEATURES
    + NUMERIC_FEATURES
    + ORDINAL_FEATURES
    + BINARY_CATEGORICAL_FEATURES
    + NOMINAL_CATEGORICAL_FEATURES
)
