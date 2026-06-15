import sqlite3

import pandas as pd

from common import PROCESSED_DIR, RAW_DATA, SQL_DIR, ensure_directories


def tenure_bucket(tenure: int) -> str:
    if tenure <= 12:
        return "0-12 months"
    if tenure <= 24:
        return "13-24 months"
    if tenure <= 48:
        return "25-48 months"
    return "49+ months"


def monthly_charge_bucket(monthly_charge: float) -> str:
    if monthly_charge < 35:
        return "Low"
    if monthly_charge < 70:
        return "Medium"
    return "High"


def risk_segment(row: pd.Series) -> str:
    score = 0
    if row["Contract"] == "Month-to-month":
        score += 2
    if row["tenure"] <= 12:
        score += 2
    if row["MonthlyCharges"] >= 70:
        score += 1
    if row["PaymentMethod"] == "Electronic check":
        score += 1
    if row["OnlineSecurity"] == "No":
        score += 1
    if row["TechSupport"] == "No":
        score += 1

    if score >= 5:
        return "High"
    if score >= 3:
        return "Medium"
    return "Low"


def clean_telco_data() -> pd.DataFrame:
    df = pd.read_csv(RAW_DATA)
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"].replace(" ", pd.NA), errors="coerce")
    df["TotalCharges"] = df["TotalCharges"].fillna(df["MonthlyCharges"])
    df["ChurnFlag"] = df["Churn"].map({"Yes": 1, "No": 0})
    df["tenure_bucket"] = df["tenure"].apply(tenure_bucket)
    df["monthly_charge_bucket"] = df["MonthlyCharges"].apply(monthly_charge_bucket)
    df["risk_segment"] = df.apply(risk_segment, axis=1)
    df["revenue_at_risk"] = df["MonthlyCharges"] * df["ChurnFlag"]
    return df


def save_outputs(df: pd.DataFrame) -> None:
    ensure_directories()
    cleaned_csv = PROCESSED_DIR / "telco_churn_clean.csv"
    sqlite_path = PROCESSED_DIR / "telco_churn.db"

    df.to_csv(cleaned_csv, index=False)

    db_df = df.rename(
        columns={
            "customerID": "customer_id",
            "SeniorCitizen": "senior_citizen",
            "PhoneService": "phone_service",
            "MultipleLines": "multiple_lines",
            "InternetService": "internet_service",
            "OnlineSecurity": "online_security",
            "OnlineBackup": "online_backup",
            "DeviceProtection": "device_protection",
            "TechSupport": "tech_support",
            "StreamingTV": "streaming_tv",
            "StreamingMovies": "streaming_movies",
            "Contract": "contract",
            "PaperlessBilling": "paperless_billing",
            "PaymentMethod": "payment_method",
            "MonthlyCharges": "monthly_charges",
            "TotalCharges": "total_charges",
            "Churn": "churn_label",
            "ChurnFlag": "churn_flag",
        }
    )

    with sqlite3.connect(sqlite_path) as conn:
        db_df.to_sql("telco_churn", conn, if_exists="replace", index=False)
        view_sql = (SQL_DIR / "03_power_bi_input.sql").read_text(encoding="utf-8")
        conn.executescript(view_sql)


if __name__ == "__main__":
    telco_df = clean_telco_data()
    save_outputs(telco_df)
    print(f"Saved cleaned data for {len(telco_df)} customers.")
