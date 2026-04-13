import React, { useState } from "react";
import "./App.css";

function App() {
  const [form, setForm] = useState({
    age: "",
    weight: "",
    height: "",
    activity: "",
    goal: "maintain"
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(form)
      });

      const data = await res.json();
      console.log("Response:", data);

      if (data.status === "success") {
        setResult(data);
      } else {
        alert(data.message || "Something went wrong");
      }
    } catch (err) {
      console.error(err);
      alert("Error connecting to backend");
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <h1 className="title">🍎 AI Diet Recommendation</h1>

      {/* 🔹 INPUT SECTION */}
      <div className="input-section">
        <input
          name="age"
          placeholder="Age"
          value={form.age}
          onChange={handleChange}
          className="input"
        />

        <input
          name="weight"
          placeholder="Weight (kg)"
          value={form.weight}
          onChange={handleChange}
          className="input"
        />

        <input
          name="height"
          placeholder="Height (cm)"
          value={form.height}
          onChange={handleChange}
          className="input"
        />

        <input
          name="activity"
          placeholder="Activity (1.2 - 1.7)"
          value={form.activity}
          onChange={handleChange}
          className="input"
        />

        <select
          name="goal"
          value={form.goal}
          onChange={handleChange}
          className="input"
        >
          <option value="maintain">Maintain</option>
          <option value="weight_loss">Weight Loss</option>
          <option value="weight_gain">Weight Gain</option>
        </select>

        <button onClick={handleSubmit} className="button">
          {loading ? "Loading..." : "Get Diet Plan"}
        </button>
      </div>

      {/* 🔹 OUTPUT SECTION */}
      {result && result.analysis && (
        <div className="output-section">
          <h2>🔥 Calories: {result.analysis.recommended_calories}</h2>
          <h3>🎯 Goal: {result.user_input.goal}</h3>

          <h3>🩺 Disease: {result.analysis.disease}</h3>
          <h3>🥗 Diet Type: {result.analysis.diet_type}</h3>

          <p>
            <b>📋 Why this diet?</b><br />
            {result.diet_plan.reason}
          </p>

          <p>
            <b>🚫 Restrictions:</b><br />
            {result.diet_plan.restrictions}
          </p>

          <p>
            <b>🍛 Preferred Cuisine:</b>{" "}
            {result.diet_plan.preferred_cuisine}
          </p>

          <p>
            <b>📊 Health Status:</b>{" "}
            {result.health_insights.health_status}
          </p>

          <p>
            <b>💡 Advice:</b>{" "}
            {result.health_insights.advice}
          </p>

          <p>
            <b>🏃 Activity Tip:</b>{" "}
            {result.health_insights.activity_tip}
          </p>
        </div>
      )}
    </div>
  );
}

export default App;