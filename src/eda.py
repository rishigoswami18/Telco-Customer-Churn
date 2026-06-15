import json

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from common import FIGURES_DIR, METRICS_DIR, PROCESSED_DIR, ensure_directories
from data_prep import clean_telco_data


sns.set_theme(style="whitegrid")


def load_data() -> pd.DataFrame:
    cleaned_path = PROCESSED_DIR / "telco_churn_clean.csv"
    if cleaned_path.exists():
        return pd.read_csv(cleaned_path)
    return clean_telco_data()


def save_plot(fig, filename: str) -> None:
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / filename, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    ensure_directories()
    df = load_data()

    summary = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "missing_values": df.isna().sum().to_dict(),
        "churn_rate_pct": round(float(df["ChurnFlag"].mean() * 100), 2),
        "monthly_charges_mean": round(float(df["MonthlyCharges"].mean()), 2),
        "total_charges_mean": round(float(df["TotalCharges"].mean()), 2),
        "top_contract_churn": df.groupby("Contract")["ChurnFlag"].mean().sort_values(ascending=False).mul(100).round(2).to_dict(),
        "top_tenure_bucket_churn": df.groupby("tenure_bucket")["ChurnFlag"].mean().sort_values(ascending=False).mul(100).round(2).to_dict(),
    }

    with open(METRICS_DIR / "eda_summary.json", "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=df, x="Churn", hue="Churn", palette="Set2", ax=ax, legend=False)
    ax.set_title("Churn Distribution")
    save_plot(fig, "churn_distribution.png")

    fig, ax = plt.subplots(figsize=(8, 5))
    contract_churn = (
        df.groupby("Contract")["ChurnFlag"].mean().sort_values(ascending=False).mul(100).reset_index()
    )
    sns.barplot(
        data=contract_churn,
        x="Contract",
        y="ChurnFlag",
        hue="Contract",
        palette="Blues_d",
        ax=ax,
        legend=False,
    )
    ax.set_title("Churn Rate by Contract Type")
    ax.set_ylabel("Churn Rate (%)")
    ax.set_xlabel("")
    save_plot(fig, "churn_by_contract.png")

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df, x="Churn", y="MonthlyCharges", hue="Churn", palette="Set3", ax=ax, legend=False)
    ax.set_title("Monthly Charges by Churn")
    save_plot(fig, "monthly_charges_by_churn.png")

    fig, ax = plt.subplots(figsize=(10, 5))
    tenure_churn = (
        df.groupby("tenure_bucket")["ChurnFlag"].mean().reindex(
            ["0-12 months", "13-24 months", "25-48 months", "49+ months"]
        ).mul(100).reset_index()
    )
    sns.barplot(
        data=tenure_churn,
        x="tenure_bucket",
        y="ChurnFlag",
        hue="tenure_bucket",
        palette="Greens_d",
        ax=ax,
        legend=False,
    )
    ax.set_title("Churn Rate by Tenure Bucket")
    ax.set_ylabel("Churn Rate (%)")
    ax.set_xlabel("")
    save_plot(fig, "churn_by_tenure_bucket.png")

    numeric_df = df[["tenure", "MonthlyCharges", "TotalCharges", "ChurnFlag"]]
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(numeric_df.corr(numeric_only=True), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    ax.set_title("Numeric Correlation Heatmap")
    save_plot(fig, "numeric_correlation_heatmap.png")

    print("EDA outputs saved.")


if __name__ == "__main__":
    main()
