# Heart disease risk check (Flask)

Flask front end for the logistic regression model in `LogisticRegression.ipynb`.

## Run
```bash
pip install -r requirements.txt
python app.py          # then open http://127.0.0.1:5000
```
The model trains automatically on first start (80/20 split, `random_state=42`, as in the notebook)
and is cached in `model.joblib`. Delete that file or run `python model.py` to retrain.

## Files
- `app.py` - routes (`/` page, `POST /predict` JSON API) and input validation
- `model.py` - training and loading
- `templates/index.html`, `static/style.css`, `static/app.js` - UI
- `heart.csv` - dataset

## API
`POST /predict` with the 13 feature values as JSON returns `{"prediction": 0|1, "probability": 0.0-1.0}`.
