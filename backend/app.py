from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from recommender import recommend_foods

app = Flask(__name__)

# ✅ Proper CORS
CORS(app)

# Load model safely
try:
    model = joblib.load("models/calorie_model.pkl")
except Exception as e:
    print("Model load error:", e)
    model = None

@app.route('/')
def home():
    return "✅ Diet Recommendation API Running"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        print("Incoming Data:", data)

        # ✅ Safe input handling
        age = float(data.get('age', 0))
        weight = float(data.get('weight', 0))
        height = float(data.get('height', 0))
        activity = float(data.get('activity', 1.2))
        goal = data.get('goal', 'maintain')

        # ✅ Model prediction
        input_data = np.array([[age, weight, height, activity]])
        calories = model.predict(input_data)[0]

        # ✅ Recommendation
        foods = recommend_foods(calories, goal)

        return jsonify({
            "calories": round(calories, 2),
            "goal": goal,
            "recommended_foods": foods
        })

    except Exception as e:
        print("🔥 ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)