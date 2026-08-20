import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

# Prototype/synthetic training data.
# Replace with real TownKart interaction data when available.
data = [
    [1.2, 320, 500, 15, 10, 1],
    [0.8, 280, 500, 4, 10, 0],
    [3.5, 350, 500, 20, 10, 1],
    [4.8, 450, 500, 2, 10, 0],
    [1.5, 400, 500, 12, 10, 1],
    [2.8, 450, 500, 15, 10, 1],
    [4.2, 300, 500, 3, 10, 0],
    [0.5, 490, 500, 20, 10, 1],
    [1.0, 700, 800, 12, 10, 1],
    [4.5, 650, 800, 3, 10, 0],
    [2.0, 600, 800, 15, 10, 1],
    [3.8, 780, 800, 20, 10, 1],
    [0.7, 750, 800, 2, 10, 0],
    [1.2, 100, 150, 30, 5, 1],
    [4.0, 80, 150, 2, 5, 0],
    [2.5, 120, 150, 10, 5, 1],
]

columns = [
    "distance_km",
    "price",
    "budget",
    "stock",
    "required_quantity",
    "selected",
]

df = pd.DataFrame(data, columns=columns)

X = df[
    ["distance_km", "price", "budget", "stock", "required_quantity"]
]
y = df["selected"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=6,
    random_state=42,
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)
print("Accuracy:", round(accuracy_score(y_test, predictions), 3))
print(classification_report(y_test, predictions, zero_division=0))

os.makedirs("ml", exist_ok=True)
joblib.dump(model, "ml/townkart_ranker.pkl")
print("Saved: ml/townkart_ranker.pkl")