import pandas as pd

def load_player_stats(file_path):
    return pd.read_csv(file_path)

def load_fixtures(file_path):
    return pd.read_csv(file_path)

def preprocess_data(player_stats, fixtures):
    # Define the target variable (example: form adjusted by fixture difficulty)
    player_stats['target'] = player_stats['form'] - player_stats['team_h_difficulty'].fillna(0)  # Replace missing values with 0
    
    # One-hot encode categorical features
    player_stats = pd.get_dummies(player_stats, columns=["position"], dummy_na=True, drop_first=True)
    
    # Select features (excluding id and target)
    features = player_stats.drop(columns=["id", "target", "player_name"])
    target = player_stats["target"]
    
    return features, target
