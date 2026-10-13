"""Train / load the logistic regression model from the notebook."""
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

BASE = Path(__file__).parent
DATA_PATH = BASE / "heart.csv"
MODEL_PATH = BASE / "model.joblib"
METRICS_PATH = BASE / "metrics.json"

FEATURES = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
            "thalach", "exang", "oldpeak", "slope", "ca", "thal"]


def train():
    """Same steps as LogisticRegression.ipynb: 80/20 split, random_state=42."""
    df = pd.read_csv(DATA_PATH)
    X = df.drop("target", axis=1)
    y = df["target"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    # max_iter raised from the default (100) so the solver converges on unscaled data
    model = LogisticRegression(max_iter=5000)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    report = classification_report(y_test, pred, output_dict=True)
    metrics = {
        "accuracy": accuracy_score(y_test, pred),
        "confusion_matrix": confusion_matrix(y_test, pred).tolist(),
        "precision": report["weighted avg"]["precision"],
        "recall": report["weighted avg"]["recall"],
        "f1": report["weighted avg"]["f1-score"],
        "train_rows": len(X_train),
        "test_rows": len(X_test),
    }
    joblib.dump(model, MODEL_PATH)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2))
    return model, metrics


def load():
    if MODEL_PATH.exists() and METRICS_PATH.exists():
        return joblib.load(MODEL_PATH), json.loads(METRICS_PATH.read_text())
    return train()


if __name__ == "__main__":
    _, m = train()
    print(json.dumps(m, indent=2))
