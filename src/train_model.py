import json

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from common import FIGURES_DIR, METRICS_DIR, MODELS_DIR, PROCESSED_DIR, ensure_directories
from data_prep import clean_telco_data

try:
    from imblearn.over_sampling import SMOTE
except ImportError:
    SMOTE = None


sns.set_theme(style="whitegrid")


def load_data() -> pd.DataFrame:
    cleaned_path = PROCESSED_DIR / "telco_churn_clean.csv"
    if cleaned_path.exists():
        return pd.read_csv(cleaned_path)
    return clean_telco_data()


def build_preprocessor(numeric_features, categorical_features):
    numeric_transformer = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )


def evaluate_model(model, x_test, y_test):
    predictions = model.predict(x_test)
    probabilities = model.predict_proba(x_test)[:, 1]
    return {
        "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
        "precision": round(float(precision_score(y_test, predictions)), 4),
        "recall": round(float(recall_score(y_test, predictions)), 4),
        "f1": round(float(f1_score(y_test, predictions)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, probabilities)), 4),
    }, predictions, probabilities


def plot_confusion_matrix(y_test, predictions, filename: str) -> None:
    fig, ax = plt.subplots(figsize=(5, 4))
    cm = confusion_matrix(y_test, predictions)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_title("Confusion Matrix")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / filename, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    ensure_directories()
    df = load_data()

    target = "ChurnFlag"
    drop_columns = ["customerID", "Churn", "revenue_at_risk", "risk_segment"]
    feature_df = df.drop(columns=drop_columns)
    x = feature_df.drop(columns=[target])
    y = feature_df[target]

    numeric_features = ["SeniorCitizen", "tenure", "MonthlyCharges", "TotalCharges"]
    categorical_features = [column for column in x.columns if column not in numeric_features]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    preprocessor = build_preprocessor(numeric_features, categorical_features)

    logistic_model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced")),
        ]
    )
    logistic_model.fit(x_train, y_train)
    logistic_metrics, logistic_predictions, logistic_probabilities = evaluate_model(
        logistic_model, x_test, y_test
    )

    x_train_prepared = preprocessor.fit_transform(x_train)
    x_test_prepared = preprocessor.transform(x_test)

    y_train_balanced = y_train
    smote_used = False
    if SMOTE is not None:
        sampler = SMOTE(random_state=42)
        x_train_prepared, y_train_balanced = sampler.fit_resample(x_train_prepared, y_train)
        smote_used = True

    random_forest = RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        min_samples_leaf=3,
        random_state=42,
        class_weight=None if smote_used else "balanced",
    )
    random_forest.fit(x_train_prepared, y_train_balanced)

    rf_predictions = random_forest.predict(x_test_prepared)
    rf_probabilities = random_forest.predict_proba(x_test_prepared)[:, 1]
    random_forest_metrics = {
        "accuracy": round(float(accuracy_score(y_test, rf_predictions)), 4),
        "precision": round(float(precision_score(y_test, rf_predictions)), 4),
        "recall": round(float(recall_score(y_test, rf_predictions)), 4),
        "f1": round(float(f1_score(y_test, rf_predictions)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, rf_probabilities)), 4),
    }

    metrics = {
        "dataset_rows": int(len(df)),
        "test_rows": int(len(x_test)),
        "smote_used": smote_used,
        "logistic_regression": logistic_metrics,
        "random_forest": random_forest_metrics,
    }

    with open(METRICS_DIR / "model_metrics.json", "w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2)

    feature_names = preprocessor.get_feature_names_out()
    importance_df = (
        pd.DataFrame({"feature": feature_names, "importance": random_forest.feature_importances_})
        .sort_values("importance", ascending=False)
        .head(15)
    )
    importance_df.to_csv(METRICS_DIR / "feature_importance.csv", index=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=importance_df,
        x="importance",
        y="feature",
        hue="feature",
        palette="viridis",
        ax=ax,
        legend=False,
    )
    ax.set_title("Top Random Forest Feature Importances")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "feature_importance.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    plot_confusion_matrix(y_test, rf_predictions, "confusion_matrix_random_forest.png")

    predictions_df = x_test.copy()
    predictions_df["actual_churn"] = y_test.values
    predictions_df["predicted_churn"] = rf_predictions
    predictions_df["churn_probability"] = rf_probabilities.round(4)
    predictions_df["retention_priority"] = pd.cut(
        predictions_df["churn_probability"],
        bins=[-0.01, 0.33, 0.66, 1.0],
        labels=["Low", "Medium", "High"],
    )
    predictions_df.to_csv(METRICS_DIR / "test_predictions.csv", index=False)

    joblib.dump(logistic_model, MODELS_DIR / "logistic_regression.joblib")
    joblib.dump(
        {
            "preprocessor": preprocessor,
            "random_forest": random_forest,
            "feature_names": feature_names,
        },
        MODELS_DIR / "random_forest.joblib",
    )

    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
