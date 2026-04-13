import pandas as pd

def recommend_foods(calories, goal="maintain"):
    df = pd.read_csv("data/diet_recommendations_dataset.csv")

    # Normalize columns
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # Use correct columns from your dataset
    if 'diet_recommendation' not in df.columns:
        raise Exception("❌ 'diet_recommendation' column not found")

    # Optional: filter by calorie similarity
    if 'daily_caloric_intake' in df.columns:
        df = df[
            (df['daily_caloric_intake'] > calories - 200) &
            (df['daily_caloric_intake'] < calories + 200)
        ]

    # Optional: goal-based filtering
    if goal == "weight_loss":
        df = df[df['dietary_nutrient_imbalance_score'] > 0.5]
    elif goal == "weight_gain":
        df = df[df['dietary_nutrient_imbalance_score'] < 0.5]

    # If empty → fallback
    if df.empty:
        df = pd.read_csv("data/diet_recommendations_dataset.csv")

    # Return diet recommendations
    recommendations = df['diet_recommendation'].dropna().unique()[:5]

    return [{"diet": r} for r in recommendations]