import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
import logging

def train_model():
    # Load the data
    data_path = 'C:/Users/Adam.Wisker/Documents/FPL-APP-Project/data/enhanced_fpl_players.csv'
    data = pd.read_csv(data_path)
    
    # Define feature columns and target
    feature_columns = [
        'minutes', 'goals_scored', 'assists', 'clean_sheets', 'goals_conceded',
        'own_goals', 'penalties_saved', 'penalties_missed', 'yellow_cards',
        'red_cards', 'saves', 'bonus', 'bps', 'influence', 'creativity', 'threat',
        'ict_index', 'starts', 'expected_goals', 'expected_assists',
        'expected_goal_involvements', 'expected_goals_conceded', 'form', 'now_cost'
    ]
    
    target_column = 'total_points'

    # Ensure 'web_name' is included in the dataset for identification
    if 'web_name' not in data.columns:
        logging.error("'web_name' column not found in data.")
        return

    # Filter the data
    data = data[feature_columns + [target_column, 'web_name']]

    # Drop rows with missing target
    data = data.dropna(subset=[target_column])

    # Split the data into training and testing sets
    X = data[feature_columns]
    y = data[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save the model
    joblib.dump(model, 'models/trained_model.pkl')
    logging.info("Model trained and saved successfully.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    train_model()
