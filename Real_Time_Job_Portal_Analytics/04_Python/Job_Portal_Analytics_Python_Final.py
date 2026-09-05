# ============================================================
# JOB PORTAL ANALYTICS - PYTHON ANALYSIS
# Primary dataset: real web-scraped job listings
# Candidate dataset: Used only for placement prediction
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


# ============================================================
# 1. LOAD THE REAL WEB-SCRAPED JOB DATASET
# ============================================================

df = pd.read_csv("Jobs_SQL.csv")

print("Dataset Shape:", df.shape)

print("\nFirst 5 Rows:")
print(df.head())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:", df.duplicated().sum())
print("Duplicate Job IDs:", df["Job ID"].duplicated().sum())


# ============================================================
# 2. BASIC DATASET SUMMARY
# ============================================================

print("\nUnique Job Titles:", df["Job Title"].nunique())
print("Unique Companies:", df["Company Name"].nunique())
print("Unique Cities:", df["City"].nunique())
print("Unique Industries:", df["Industry"].nunique())
print("Unique IT Categories:", df["IT Job Category"].nunique())
print("Unique Experience Levels:", df["Experience Category"].nunique())
print("Unique Work Modes:", df["Work Mode"].nunique())


# ============================================================
# 3. TOP 10 JOB ROLES
# ============================================================

top_roles = df["Job Title"].value_counts().head(10)

print("\nTop 10 Job Roles:")
print(top_roles)

top_roles.plot(kind="bar", color="skyblue")
plt.title("Top 10 Job Roles by Demand")
plt.xlabel("Job Title")
plt.ylabel("Number of Jobs")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# ============================================================
# 4. TOP 10 HIRING CITIES
# ============================================================

top_cities = df["City"].value_counts().head(10)

print("\nTop 10 Hiring Cities:")
print(top_cities)

top_cities.plot(kind="bar", color="lightgreen")
plt.title("Top 10 Hiring Cities")
plt.xlabel("City")
plt.ylabel("Number of Jobs")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# ============================================================
# 5. TOP 10 SKILLS
# ============================================================

skills = df["Skills Required"].str.split(", ").explode()
top_skills = skills.value_counts().head(10)

print("\nTop 10 Skills:")
print(top_skills)

top_skills.plot(kind="bar", color="plum")
plt.title("Top 10 Most Requested Skills")
plt.xlabel("Skill")
plt.ylabel("Number of Job Mentions")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# ============================================================
# 6. EXPERIENCE LEVEL
# ============================================================

experience = df["Experience Category"].value_counts()

print("\nExperience Level Demand:")
print(experience)

experience.plot(kind="bar", color="orange")
plt.title("Job Demand by Experience Level")
plt.xlabel("Experience Level")
plt.ylabel("Number of Jobs")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# ============================================================
# 7. INDUSTRY
# ============================================================

industry = df["Industry"].value_counts()

print("\nIndustry Demand:")
print(industry)

industry.plot(kind="bar", color="lightcoral")
plt.title("IT Job Demand by Industry")
plt.xlabel("Industry")
plt.ylabel("Number of Jobs")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# ============================================================
# 8. WORK MODE
# ============================================================

work_mode = df["Work Mode"].value_counts()

print("\nWork Mode:")
print(work_mode)

# The current dataset has only one work mode.
# A chart is created only when there is more than one category.
if len(work_mode) > 1:
    work_mode.plot(kind="bar", color="gold")
    plt.title("Job Distribution by Work Mode")
    plt.xlabel("Work Mode")
    plt.ylabel("Number of Jobs")
    plt.tight_layout()
    plt.show()
else:
    print("Work Mode chart skipped because only one work mode exists.")


# ============================================================
# 9. SALARY ANALYSIS
# ============================================================

salary_df = df[df["Salary Available"] == "Yes"].copy()

print("\nSalary Records:", len(salary_df))

print("\nSalary Statistics:")
print(
    salary_df[
        ["Salary Min", "Salary Max", "Salary Average"]
    ].describe()
)

print(
    "\nSalary Min greater than Salary Max:",
    (salary_df["Salary Min"] > salary_df["Salary Max"]).sum()
)

print(
    "Salary Average outside Min-Max:",
    (
        (salary_df["Salary Average"] < salary_df["Salary Min"]) |
        (salary_df["Salary Average"] > salary_df["Salary Max"])
    ).sum()
)


# Average salary by job title
salary_by_role = (
    salary_df.groupby("Job Title")["Salary Average"]
    .mean()
    .sort_values(ascending=False)
)

print("\nAverage Salary by Job Title:")
print(salary_by_role)

salary_by_role.plot(
    kind="bar",
    color="mediumpurple"
)
plt.title("Average Salary by Job Title")
plt.xlabel("Job Title")
plt.ylabel("Average Salary")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# ============================================================
# 10. NUMPY ANALYSIS
# ============================================================

applicants = df["Number of Applicants"].to_numpy()

print("\nNumPy Applicant Analysis:")
print("Total Applicants:", np.sum(applicants))
print("Average Applicants:", np.mean(applicants))
print("Maximum Applicants:", np.max(applicants))
print("Minimum Applicants:", np.min(applicants))

salary_values = salary_df["Salary Average"].to_numpy()

print("\nNumPy Salary Analysis:")
print("Average Salary:", np.mean(salary_values))
print("Median Salary:", np.median(salary_values))
print("Minimum Salary:", np.min(salary_values))
print("Maximum Salary:", np.max(salary_values))


# ============================================================
# 11. CLEAN ANALYSIS DATAFRAME + DATE
# ============================================================

analysis_df = df.copy()

analysis_df["analysis_date"] = pd.to_datetime(
    analysis_df["Posted Date"]
)

print(
    "\nMissing Analysis Dates:",
    analysis_df["analysis_date"].isnull().sum()
)


# ============================================================
# 12. SALARY PREDICTION
# ============================================================

# Only jobs with salary information are used.
ml_salary_df = analysis_df[
    analysis_df["Salary Available"] == "Yes"
].copy()

model_data = ml_salary_df[
    [
        "Job Title",
        "City",
        "Industry",
        "Experience Category",
        "Seniority Level",
        "Job Type",
        "Salary Average"
    ]
].copy()

X = model_data[
    [
        "Job Title",
        "City",
        "Industry",
        "Experience Category",
        "Seniority Level",
        "Job Type"
    ]
]

y = model_data["Salary Average"]


# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Categorical columns
categorical_columns = [
    "Job Title",
    "City",
    "Industry",
    "Experience Category",
    "Seniority Level",
    "Job Type"
]


# Convert text columns into numbers
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_columns
        )
    ]
)


# ---------------- Linear Regression ----------------

linear_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("regressor", LinearRegression())
    ]
)

linear_model.fit(X_train, y_train)

linear_pred = linear_model.predict(X_test)

linear_mae = mean_absolute_error(y_test, linear_pred)
linear_rmse = np.sqrt(
    mean_squared_error(y_test, linear_pred)
)
linear_r2 = r2_score(y_test, linear_pred)

print("\nLinear Regression:")
print("MAE:", round(linear_mae, 2))
print("RMSE:", round(linear_rmse, 2))
print("R2:", round(linear_r2, 2))


# ---------------- Random Forest ----------------

rf_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "regressor",
            RandomForestRegressor(
                n_estimators=100,
                random_state=42
            )
        )
    ]
)

rf_model.fit(X_train, y_train)

rf_pred = rf_model.predict(X_test)

rf_mae = mean_absolute_error(y_test, rf_pred)
rf_rmse = np.sqrt(
    mean_squared_error(y_test, rf_pred)
)
rf_r2 = r2_score(y_test, rf_pred)

print("\nRandom Forest:")
print("MAE:", round(rf_mae, 2))
print("RMSE:", round(rf_rmse, 2))
print("R2:", round(rf_r2, 2))


# ---------------- Model Comparison ----------------

model_comparison = pd.DataFrame({
    "Model": [
        "Linear Regression",
        "Random Forest"
    ],
    "MAE": [
        linear_mae,
        rf_mae
    ],
    "RMSE": [
        linear_rmse,
        rf_rmse
    ],
    "R2 Score": [
        linear_r2,
        rf_r2
    ]
})

print("\nSalary Model Comparison:")
print(model_comparison.round(2))


# ---------------- Actual vs Predicted ----------------

plt.scatter(
    y_test,
    rf_pred,
    color="purple",
    marker="o"
)

plt.title("Actual vs Predicted Salary")
plt.xlabel("Actual Salary")
plt.ylabel("Predicted Salary")
plt.tight_layout()
plt.show()


# ============================================================
# 13. CURRENT JOB DEMAND ANALYSIS
# ============================================================

# These are the final business-question outputs.
# No extra analysis is performed here.

print("\nTop Current Job Roles:")
print(top_roles)

print("\nTop Current Skills:")
print(top_skills)

print("\nTop Hiring Cities:")
print(top_cities)

print("\nTop Industries:")
print(industry)

print("\nDemand by Experience:")
print(experience)


# ============================================================
# 14. JOB-DEMAND FORECASTING FEASIBILITY
# ============================================================

unique_dates = (
    analysis_df["analysis_date"]
    .dt.date
    .nunique()
)

print("\nUnique Analysis Dates:", unique_dates)
print("Start Date:", analysis_df["analysis_date"].min())
print("End Date:", analysis_df["analysis_date"].max())

if unique_dates < 30:
    print(
        "Job-demand forecasting is not performed "
        "because sufficient historical time variation is unavailable."
    )


# ============================================================
# 15. CANDIDATE PLACEMENT PREDICTION
# ============================================================
# This is the ONLY synthetic dataset in the project.

candidate_df = pd.read_csv(
    "Vetri_Candidate_Profiles.csv"
)

print("\nCandidate Dataset Shape:", candidate_df.shape)

print("\nShortlist Status:")
print(candidate_df["Shortlist Status"].value_counts())


# Select only the required candidate fields
candidate_model_data = candidate_df[
    [
        "Age",
        "Gender",
        "Highest Education",
        "Total Experience Years",
        "Skills",
        "Target Role",
        "Expected Salary LPA",
        "Preferred Location",
        "Preferred Work Mode",
        "Shortlist Status"
    ]
].copy()


# Separate features and target
X_candidate = candidate_model_data.drop(
    "Shortlist Status",
    axis=1
)

y_candidate = candidate_model_data["Shortlist Status"]


# Split candidate data
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
    X_candidate,
    y_candidate,
    test_size=0.2,
    random_state=42,
    stratify=y_candidate
)


# Candidate numeric columns
numeric_columns = [
    "Age",
    "Total Experience Years",
    "Expected Salary LPA"
]


# Candidate text columns
candidate_categorical_columns = [
    "Gender",
    "Highest Education",
    "Skills",
    "Target Role",
    "Preferred Location",
    "Preferred Work Mode"
]


# Convert candidate text fields into numbers
candidate_preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            "passthrough",
            numeric_columns
        ),
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            candidate_categorical_columns
        )
    ]
)


# Simple classification model
candidate_model = Pipeline(
    steps=[
        ("preprocessor", candidate_preprocessor),
        (
            "classifier",
            LogisticRegression(
                class_weight="balanced",
                max_iter=1000
            )
        )
    ]
)


# Train the model
candidate_model.fit(
    X_train_c,
    y_train_c
)


# Make predictions
candidate_pred = candidate_model.predict(X_test_c)


# ============================================================
# 16. CANDIDATE MODEL EVALUATION
# ============================================================

accuracy = accuracy_score(
    y_test_c,
    candidate_pred
)

precision = precision_score(
    y_test_c,
    candidate_pred,
    pos_label="Not Shortlisted",
    zero_division=0
)

recall = recall_score(
    y_test_c,
    candidate_pred,
    pos_label="Not Shortlisted",
    zero_division=0
)

f1 = f1_score(
    y_test_c,
    candidate_pred,
    pos_label="Not Shortlisted",
    zero_division=0
)

print("\nCandidate Placement Prediction:")
print("Accuracy:", round(accuracy, 2))
print("Precision:", round(precision, 2))
print("Recall:", round(recall, 2))
print("F1 Score:", round(f1, 2))

print("\nConfusion Matrix:")
print(
    confusion_matrix(
        y_test_c,
        candidate_pred
    )
)


# ============================================================
# END OF PROJECT
# ============================================================

print("\nPython analysis completed successfully.")
