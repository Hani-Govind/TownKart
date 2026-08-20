import joblib
import pandas as pd

MODEL_PATH = "ml/townkart_ranker.pkl"
model = joblib.load(MODEL_PATH)

def predict_match(
    distance_km,
    price,
    budget,
    stock,
    required_quantity,
):
    features = pd.DataFrame([{
        "distance_km": distance_km,
        "price": price,
        "budget": budget if budget is not None else 0,
        "stock": stock,
        "required_quantity": (
            required_quantity if required_quantity is not None else 1
        ),
    }])

    probability = model.predict_proba(features)[0][1]
    return round(float(probability) * 100, 2)
