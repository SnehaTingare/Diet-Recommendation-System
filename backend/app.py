from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from recommender import recommend_foods

app = Flask(__name__)

# ✅ Enable CORS with explicit settings
CORS(app, 
    resources={r"/*": {"origins": "*"}},
    methods=['GET', 'POST', 'OPTIONS'],
    allow_headers=['Content-Type'])

# ✅ Load our new Assets
try:
    # Note: Using pickle as we did in Jupyter, not joblib
    with open("diet_model.pkl", "rb") as f:
        knn_model = pickle.load(f)
    print("✅ KNN Model loaded successfully")
except Exception as e:
    print("❌ Model load error:", e)
    knn_model = None

@app.route('/')
def home():
    return "✅ AI Diet Recommendation API Running"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        print("📥 Incoming Data:", data)

        # ✅ Extract Inputs
        age = float(data.get('age', 0))
        weight = float(data.get('weight', 0))
        height = float(data.get('height', 0))
        gender = data.get('gender', 'male')
        activity = float(data.get('activity', 1.2))
        goal = data.get('goal', 'maintain')
        disease = data.get('disease', 'Healthy')

        # Adjust for Goal
        if goal == 'lose': calories = tdee - 500
        elif goal == 'gain': calories = tdee + 500
        else: calories = tdee

        # ✅ 2. Get recommendations from our ML KNN Engine
        # This calls the new recommender.py we just updated
        plan = recommend_foods(calories, medical_condition=condition, goal=goal)

        # ✅ Get detailed plan from dataset
        plan = recommend_foods(calories, goal, disease)

        # ✅ 3. Structured Response for React Frontend
        response = {
            "status": "success",
            "user_input": {
                "age": age,
                "weight": weight,
                "height": height,
                "activity": activity,
                "goal": goal,
                "disease": disease
            },
            "analysis": {
                "bmi": round(weight / ((height/100)**2), 2),
                "recommended_calories": round(calories, 2),
                "medical_profile": condition
            },
            "recommendations": plan.get("recommendations"),
            "insights": {
                "health_status": plan.get("health_status"),
                "advice": plan.get("advice")
            }
        }

        return jsonify(response)

    except Exception as e:
        print("🔥 ERROR:", str(e))
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)