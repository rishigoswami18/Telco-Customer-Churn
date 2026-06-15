from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RAW_DATA = DATA_DIR / "Telco-Customer-Churn.csv"
PROCESSED_DIR = DATA_DIR / "processed"
ARTIFACTS_DIR = ROOT / "artifacts"
FIGURES_DIR = ARTIFACTS_DIR / "figures"
METRICS_DIR = ARTIFACTS_DIR / "metrics"
MODELS_DIR = ARTIFACTS_DIR / "models"
SQL_DIR = ROOT / "sql"


def ensure_directories() -> None:
    for path in [PROCESSED_DIR, FIGURES_DIR, METRICS_DIR, MODELS_DIR]:
        path.mkdir(parents=True, exist_ok=True)
