from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from recommender import recommend_foods

app = Flask(__name__)

# ✅ Enable CORS
CORS(app)

# ✅ Load model safely
try:
    model = joblib.load("models/calorie_model.pkl")
    print("✅ Model loaded successfully")
except Exception as e:
    print("❌ Model load error:", e)
    model = None

@app.route('/')
def home():
    return "✅ AI Diet Recommendation API Running"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        print("📥 Incoming Data:", data)

        # ✅ Safe input handling
        age = float(data.get('age', 0))
        weight = float(data.get('weight', 0))
        height = float(data.get('height', 0))
        activity = float(data.get('activity', 1.2))
        goal = data.get('goal', 'maintain')

        # ✅ Model prediction
        if model is None:
            raise Exception("Model not loaded properly")

        input_data = np.array([[age, weight, height, activity]])
        calories = model.predict(input_data)[0]

        # ✅ Get detailed plan from dataset
        plan = recommend_foods(calories, goal)

        # ✅ Structured response
        response = {
            "status": "success",
            "user_input": {
                "age": age,
                "weight": weight,
                "height": height,
                "activity": activity,
                "goal": goal
            },
            "analysis": {
                "recommended_calories": round(calories, 2),
                "diet_type": plan.get("diet_type"),
                "disease": plan.get("disease")
            },
            "diet_plan": {
                "reason": plan.get("reason"),
                "restrictions": plan.get("restrictions"),
                "preferred_cuisine": plan.get("cuisine")
            },
            "health_insights": {
                "health_status": plan.get("health_status"),
                "advice": plan.get("advice"),
                "activity_tip": plan.get("activity_tip")
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
    app.run(debug=True)