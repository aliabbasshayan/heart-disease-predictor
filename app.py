from flask import Flask, jsonify, render_template, request
import pandas as pd

from model import FEATURES, load

app = Flask(__name__)
model, metrics = load()

# Form fields: label, type, and allowed range / options (also used for validation)
FIELDS = [
    {"name": "age", "label": "Age", "unit": "years", "type": "number", "min": 1, "max": 120, "step": 1, "example": 54},
    {"name": "sex", "label": "Sex", "type": "select", "options": [(1, "Male"), (0, "Female")], "example": 1},
    {"name": "cp", "label": "Chest pain type", "type": "select",
     "options": [(0, "Typical angina"), (1, "Atypical angina"), (2, "Non-anginal pain"), (3, "No symptoms")], "example": 0},
    {"name": "trestbps", "label": "Resting blood pressure", "unit": "mm Hg", "type": "number", "min": 50, "max": 260, "step": 1, "example": 130},
    {"name": "chol", "label": "Cholesterol", "unit": "mg/dl", "type": "number", "min": 80, "max": 700, "step": 1, "example": 240},
    {"name": "fbs", "label": "Fasting blood sugar above 120 mg/dl", "type": "select", "options": [(0, "No"), (1, "Yes")], "example": 0},
    {"name": "restecg", "label": "Resting ECG result", "type": "select",
     "options": [(0, "Normal"), (1, "ST-T wave abnormality"), (2, "Left ventricular hypertrophy")], "example": 1},
    {"name": "thalach", "label": "Maximum heart rate reached", "unit": "bpm", "type": "number", "min": 40, "max": 250, "step": 1, "example": 150},
    {"name": "exang", "label": "Chest pain during exercise", "type": "select", "options": [(0, "No"), (1, "Yes")], "example": 0},
    {"name": "oldpeak", "label": "ST depression after exercise", "unit": "mm", "type": "number", "min": 0, "max": 10, "step": 0.1, "example": 1.0},
    {"name": "slope", "label": "Slope of the ST segment", "type": "select",
     "options": [(0, "Upsloping"), (1, "Flat"), (2, "Downsloping")], "example": 1},
    {"name": "ca", "label": "Major vessels colored by fluoroscopy", "type": "select",
     "options": [(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4")], "example": 0},
    {"name": "thal", "label": "Thalassemia test result", "type": "select",
     "options": [(0, "Not recorded"), (1, "Fixed defect"), (2, "Normal"), (3, "Reversible defect")], "example": 2},
]
FIELD_MAP = {f["name"]: f for f in FIELDS}


def parse(payload):
    """Validate the request and return (values, errors)."""
    values, errors = {}, {}
    for f in FIELDS:
        raw = payload.get(f["name"])
        if raw in (None, ""):
            errors[f["name"]] = "Enter a value."
            continue
        try:
            num = float(raw)
        except (TypeError, ValueError):
            errors[f["name"]] = "Enter a number."
            continue
        if f["type"] == "number":
            if not f["min"] <= num <= f["max"]:
                errors[f["name"]] = f"Enter a value between {f['min']} and {f['max']}."
                continue
        elif num not in [o[0] for o in f["options"]]:
            errors[f["name"]] = "Choose one of the options."
            continue
        values[f["name"]] = num
    return values, errors


@app.get("/")
def index():
    return render_template("index.html", fields=FIELDS, metrics=metrics)


@app.post("/predict")
def predict():
    values, errors = parse(request.get_json(silent=True) or {})
    if errors:
        return jsonify({"errors": errors}), 400
    row = pd.DataFrame([[values[c] for c in FEATURES]], columns=FEATURES)
    prob = float(model.predict_proba(row)[0][1])
    return jsonify({
        "prediction": int(prob >= 0.5),
        "probability": round(prob, 4),
    })


if __name__ == "__main__":
    app.run(debug=True)
