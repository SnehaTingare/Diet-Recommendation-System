import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Simple training data
data = pd.DataFrame({
    'age': [20, 25, 30, 35, 40],
    'weight': [50, 60, 70, 80, 90],
    'height': [150, 160, 170, 180, 175],
    'activity': [1.2, 1.3, 1.5, 1.7, 1.4],
    'calories': [1600, 1800, 2200, 2600, 2400]
})

X = data[['age', 'weight', 'height', 'activity']]
y = data['calories']

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, "models/calorie_model.pkl")

print("✅ Model trained")