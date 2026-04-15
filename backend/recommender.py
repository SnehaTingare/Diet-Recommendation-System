import pandas as pd
import numpy as np
import pickle
import os

# Load the ML assets generated in Jupyter
# Ensure these files are in the same directory or provide the correct path
MODEL_PATH = 'diet_model.pkl'
SCALER_PATH = 'scaler.pkl'
DATA_PATH = 'final_food_data.csv'

def recommend_foods(calories, medical_condition="None", goal="maintain"):
    # 1. Load the Model, Scaler, and Dataset
    if not os.path.exists(MODEL_PATH):
        return {"error": "Model files not found. Please run the Jupyter training first."}
    
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
    
    df = pd.read_csv(DATA_PATH)

    # 2. Medical Filtering (Hard Constraints)
    # This ensures we only look at foods safe for the user's condition
    condition_map = {
        'Diabetes': 'Diabetes_Friendly',
        'Heart Disease': 'Heart_Friendly',
        'Kidney Disease': 'Kidney_Friendly',
        'Liver Disease': 'Liver_Friendly'
    }
    
    if medical_condition in condition_map:
        # Filter the database to only safe foods
        filtered_df = df[df[condition_map[medical_condition]] == 1].copy()
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