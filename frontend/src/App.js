import React, { useState } from "react";
import "./App.css";
import { API_ENDPOINTS } from "./config";

function App() {
  const [form, setForm] = useState({
    age: "",
    weight: "",
    height: "",
    activity: "",
    goal: "maintain",
    disease: "Healthy"
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setError(null);
  };

  const validateForm = () => {
    const { age, weight, height, activity } = form;
    
    if (!age || !weight || !height || !activity) {
      setError("❌ Please fill in all fields");
      return false;
    }
    
    if (isNaN(age) || age <= 0 || age > 150) {
      setError("❌ Age must be between 1 and 150");
      return false;
    }
    
    if (isNaN(weight) || weight <= 0 || weight > 500) {
      setError("❌ Weight must be between 1 and 500 kg");
      return false;
    }
    
    if (isNaN(height) || height <= 0 || height > 300) {
      setError("❌ Height must be between 1 and 300 cm");
      return false;
    }
    
    if (isNaN(activity) || activity < 1.2 || activity > 1.7) {
      setError("❌ Activity level must be between 1.2 and 1.7");
      return false;
    }
    
    return true;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;

    setLoading(true);
    setError(null);

    try {
      const res = await fetch(API_ENDPOINTS.PREDICT, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          age: parseFloat(form.age),
          weight: parseFloat(form.weight),
          height: parseFloat(form.height),
          activity: parseFloat(form.activity),
          goal: form.goal,
          disease: form.disease
        })
      });

      const data = await res.json();
      console.log("Response:", data);

      if (data.status === "success") {
        setResult(data);
      } else {
        setError("❌ " + (data.message || "Something went wrong"));
      }
    } catch (err) {
      console.error(err);
      setError(`❌ Error connecting to backend at ${API_ENDPOINTS.PREDICT}. Make sure the server is running.`);
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <div className="header">
        <h1 className="title">🍎 AI Diet Recommendation System</h1>
        <p className="subtitle">Get personalized diet plans based on your health metrics</p>
      </div>

      {/* 🔹 INPUT SECTION */}
      <div className="card input-section">
        <h2 className="section-title">📋 Your Health Information</h2>

        <div className="form-group">
          <label htmlFor="age">Age (years)</label>
          <input
            id="age"
            name="age"
            type="number"
            placeholder="e.g., 25"
            value={form.age}
            onChange={handleChange}
            className="input"
            min="1"
            max="150"
          />
        </div>

        <div className="form-group">
          <label htmlFor="weight">Weight (kg)</label>
          <input
            id="weight"
            name="weight"
            type="number"
            placeholder="e.g., 70"
            value={form.weight}
            onChange={handleChange}
            className="input"
            min="1"
            max="500"
            step="0.1"
          />
        </div>

        <div className="form-group">
          <label htmlFor="height">Height (cm)</label>
          <input
            id="height"
            name="height"
            type="number"
            placeholder="e.g., 175"
            value={form.height}
            onChange={handleChange}
            className="input"
            min="1"
            max="300"
          />
        </div>

        <div className="form-group">
          <label htmlFor="activity">Activity Level</label>
          <select
            id="activity"
            name="activity"
            value={form.activity}
            onChange={handleChange}
            className="input"
          >
            <option value="">Select Activity Level</option>
            <option value="1.2">1.2 - Sedentary (little or no exercise)</option>
            <option value="1.375">1.375 - Lightly Active (exercise 1-3 days/week)</option>
            <option value="1.55">1.55 - Moderately Active (exercise 3-5 days/week)</option>
            <option value="1.725">1.725 - Very Active (exercise 6-7 days/week)</option>
            <option value="1.9">1.9 - Extremely Active (physical job)</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="goal">Your Goal</label>
          <select
            id="goal"
            name="goal"
            value={form.goal}
            onChange={handleChange}
            className="input"
          >
            <option value="maintain">🎯 Maintain Weight</option>
            <option value="weight_loss">📉 Weight Loss</option>
            <option value="weight_gain">📈 Weight Gain</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="disease">Health Condition</label>
          <select
            id="disease"
            name="disease"
            value={form.disease}
            onChange={handleChange}
            className="input"
          >
            <option value="Healthy">💚 Healthy (No Conditions)</option>
            <option value="Diabetes">🩺 Diabetes</option>
            <option value="Hypertension">🩹 Hypertension (High Blood Pressure)</option>
            <option value="Obesity">⚖️ Obesity</option>
          </select>
        </div>

        {error && <div className="error-message">{error}</div>}

        <button onClick={handleSubmit} className="button" disabled={loading}>
          {loading ? "⏳ Analyzing..." : "🚀 Get Diet Plan"}
        </button>
      </div>

      {/* 🔹 OUTPUT SECTION */}
      {result && result.analysis && (
        <div className="results">
          <div className="card result-card">
            <h2 className="section-title">⚡ Your Diet Analysis</h2>
            
            <div className="result-grid">
              <div className="result-item">
                <span className="result-label">🔥 Recommended Calories</span>
                <span className="result-value">{result.analysis.recommended_calories} kcal/day</span>
              </div>

              <div className="result-item">
                <span className="result-label">🎯 Your Goal</span>
                <span className="result-value">{result.user_input.goal.replace(/_/g, " ")}</span>
              </div>

              <div className="result-item">
                <span className="result-label">🩺 Health Condition</span>
                <span className="result-value">{result.user_input.disease}</span>
              </div>

              <div className="result-item">
                <span className="result-label">🥗 Diet Type</span>
                <span className="result-value">{result.analysis.diet_type}</span>
              </div>
            </div>
          </div>

          <div className="card result-card">
            <h2 className="section-title">🍽️ Diet Plan Details</h2>
            
            <div className="detail-section">
              <h3>📋 Why This Diet?</h3>
              <p>{result.diet_plan.reason}</p>
            </div>

            <div className="detail-section">
              <h3>🚫 Dietary Restrictions</h3>
              <p>{result.diet_plan.restrictions}</p>
            </div>

            <div className="detail-section">
              <h3>🍛 Preferred Cuisine</h3>
              <p>{result.diet_plan.cuisine || "N/A"}</p>
            </div>
          </div>

          <div className="card result-card">
            <h2 className="section-title">💪 Health Insights & Tips</h2>
            
            <div className="detail-section">
              <h3>📊 Health Status</h3>
              <p>{result.health_insights.health_status}</p>
            </div>

            <div className="detail-section">
              <h3>💡 Personalized Advice</h3>
              <p>{result.health_insights.advice}</p>
            </div>

            <div className="detail-section">
              <h3>🏃 Activity Recommendation</h3>
              <p>{result.health_insights.activity_tip}</p>
            </div>
          </div>

          <button onClick={() => setResult(null)} className="button secondary-button">
            📋 New Recommendation
          </button>
        </div>
      )}
    </div>
  );
}

export default App;