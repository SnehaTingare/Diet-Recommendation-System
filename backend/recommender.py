import pandas as pd
import numpy as np
import pickle
import os

def recommend_foods(calories, goal="maintain", disease="Healthy"):
    df = pd.read_csv("data/diet_recommendations_dataset.csv")

    # Clean column names
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # 🔥 Filter by disease type first
    if disease and disease.lower() != "healthy":
        df_filtered = df[df['disease_type'].str.lower() == disease.lower()]
    else:
        # For healthy people, exclude disease patients
        df_filtered = df[df['disease_type'].isna()]

    # 🔥 Then match similar calorie users
    df_filtered = df_filtered[
        (df_filtered['daily_caloric_intake'] > calories - 200) &
        (df_filtered['daily_caloric_intake'] < calories + 200)
    ]

    # fallback if empty - use any matching disease
    if df_filtered.empty:
        if disease and disease.lower() != "healthy":
            df_filtered = df[df['disease_type'].str.lower() == disease.lower()]
        else:
            df_filtered = df

    # 🔥 Pick best matching record
    user = df_filtered.sample(1).iloc[0]

    disease = user['disease_type']
    diet = user['diet_recommendation']
    restrictions = user['dietary_restrictions']
    cuisine = user['preferred_cuisine']
    imbalance = user['dietary_nutrient_imbalance_score']
    activity = user['physical_activity_level']
    exercise = user['weekly_exercise_hours']

    # 🔥 Reason generation (dynamic)
    reason = f"This diet is recommended for {disease} patients with {activity} activity level."

    # 🔥 Restrictions
    restriction_text = (
        f"Avoid: {restrictions}" if pd.notna(restrictions)
        else "No strict dietary restrictions"
    )

    # 🔥 Health insights
    if imbalance > 0.7:
        health_status = "High nutrient imbalance detected."
        advice = "Improve diet quality and reduce unhealthy intake."
    else:
        filtered_df = df.copy()

    if filtered_df.empty:
        filtered_df = df # Fallback if filtering is too strict

    # 3. Create Search Vector (The "Ideal" Meal)
    # We estimate a healthy macro split for the target calories
    protein_target = (calories * 0.25) / 4
    carbs_target = (calories * 0.50) / 4
    fat_target = (calories * 0.25) / 9
    fiber_target = 5.0
    sugar_target = 5.0

    # If the goal is to gain weight, we skew the search toward higher protein
    if goal == "gain":
        protein_target *= 1.2
        
    search_vector = np.array([[calories, protein_target, carbs_target, fat_target, fiber_target, sugar_target]])

    # 4. ML Search (KNN)
    # Scale the search vector using the same scaler used during training
    search_scaled = scaler.transform(search_vector)
    
    # Find the 10 nearest items
    distances, indices = model.kneighbors(search_scaled)
    
    # Get the actual food data for those indices
    recommendations = df.iloc[indices[0]]

    # 5. Cross-reference with the Medical Filter
    # Only keep recommendations that passed the medical check
    final_suggestions = recommendations[recommendations.index.isin(filtered_df.index)]

    # If KNN didn't find items in the medical list, pull directly from the filtered list
    if final_suggestions.empty:
        final_suggestions = filtered_df.sample(min(3, len(filtered_df)))

    # 6. Format the output for the UI
    # We'll take the top 3 items to show as a meal plan
    top_items = final_suggestions.head(3).to_dict(orient='records')
    
    # Logic for health status and advice
    is_diabetic = 1 if medical_condition == "Diabetes" else 0
    
    return {
        "target_calories": round(calories, 2),
        "medical_condition": medical_condition,
        "goal": goal,
        "recommendations": [
            {
                "food": item['Food_Item'],
                "calories": item['Calories (kcal)'],
                "category": item['Category'],
                "protein": item['Protein (g)'],
                "carbs": item['Carbohydrates (g)']
            } for item in top_items
        ],
        "health_status": "Personalized medical filter applied." if medical_condition != "None" else "General health guidelines applied.",
        "advice": f"For {goal}ing weight, prioritize these {len(top_items)} items which fit your {medical_condition} profile."
    }