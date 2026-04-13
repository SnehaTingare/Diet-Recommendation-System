import pandas as pd

def recommend_foods(calories, goal="maintain"):
    df = pd.read_csv("data/diet_recommendations_dataset.csv")

    # Clean column names
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # 🔥 Match similar calorie users
    df_filtered = df[
        (df['daily_caloric_intake'] > calories - 200) &
        (df['daily_caloric_intake'] < calories + 200)
    ]

    # fallback if empty
    if df_filtered.empty:
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
        health_status = "Diet is relatively balanced."
        advice = "Maintain your current healthy eating habits."

    # 🔥 Activity insight
    activity_tip = f"Recommended exercise: {exercise} hours/week"

    return {
        "diet_type": diet,
        "disease": disease,
        "reason": reason,
        "restrictions": restriction_text,
        "cuisine": cuisine,
        "health_status": health_status,
        "advice": advice,
        "activity_tip": activity_tip
    }