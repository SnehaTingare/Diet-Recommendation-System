import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle
import os

# Create directory if it doesn't exist
if not os.path.exists('models'):
    os.makedirs('models')

data = pd.DataFrame({
    'age': [20, 25, 30, 35, 40, 22, 28, 33, 45, 50],
    'weight': [50, 60, 70, 80, 90, 55, 65, 75, 85, 95],
    'height': [150, 160, 170, 180, 175, 155, 165, 172, 178, 182],
    'activity': [1.2, 1.3, 1.5, 1.7, 1.4, 1.2, 1.4, 1.6, 1.8, 1.3],
    'calories': [1600, 1800, 2200, 2600, 2400, 1700, 1950, 2300, 2700, 2500]
})

X = data[['age', 'weight', 'height', 'activity']]
y = data['calories']

model = LinearRegression()
model.fit(X, y)

# Save as pickle inside the models folder
with open("models/calorie_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Calorie Model trained and saved in models/folder")