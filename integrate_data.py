import pandas as pd
import logging
from src.data_handler import preprocess_data

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_csv(data_path: str):
    try:
        data = pd.read_csv(data_path)
        logging.info(f"Data loaded from {data_path}")
        logging.info(f"Columns in {data_path}: {data.columns.tolist()}")
        return data
    except FileNotFoundError:
        logging.error(f"File not found at {data_path}")
        return None

def merge_datasets(fpl_players, fpl_teams, understat_df, fpl_fixtures=None):
    logging.info("Merging datasets...")

    # Check if 'id' column exists in datasets
    if 'id' not in fpl_players.columns:
        logging.error("'id' column not found in fpl_players.")
        return None
    if 'id' not in understat_df.columns:
        logging.error("'id' column not found in understat_df.")
        return None
    if 'id' not in fpl_teams.columns:
        logging.error("'id' column not found in fpl_teams.")
        return None

    # Merge fpl_players with understat_players
    combined_df = fpl_players.merge(understat_df, on='id', how='left')
    logging.info(f"Columns after merging fpl_players and understat_df: {combined_df.columns.tolist()}")

    # Merge combined_df with fpl_teams
    combined_df = combined_df.merge(fpl_teams, left_on='team', right_on='id', how='left', suffixes=('', '_team'))
    logging.info(f"Columns after merging with fpl_teams: {combined_df.columns.tolist()}")

    # Handle fixtures if available
    if fpl_fixtures is not None:
        if 'name' in fpl_teams.columns and 'team_h' in fpl_fixtures.columns and 'team_a' in fpl_fixtures.columns:
            team_name_to_id = fpl_teams.set_index('name')['id'].to_dict()
            fpl_fixtures['team_h_id'] = fpl_fixtures['team_h'].map(team_name_to_id)
            fpl_fixtures['team_a_id'] = fpl_fixtures['team_a'].map(team_name_to_id)
            logging.info("Added 'team_h_id' and 'team_a_id' to fpl_fixtures based on team names.")
        else:
            logging.error("Required columns for fixture processing not found.")
            return None

        # Merge with home fixtures
        combined_df = combined_df.merge(fpl_fixtures, left_on='team', right_on='team_h_id', how='left', suffixes=('', '_home'))
        logging.info(f"Columns after merging with home fixtures: {combined_df.columns.tolist()}")

        # Merge with away fixtures
        combined_df = combined_df.merge(fpl_fixtures, left_on='team', right_on='team_a_id', how='left', suffixes=('', '_away'))
        logging.info(f"Columns after merging with away fixtures: {combined_df.columns.tolist()}")

    # Rename 'id' to 'player_id' if it exists
    if 'id' in combined_df.columns:
        combined_df = combined_df.rename(columns={'id': 'player_id'})
        logging.info(f"Columns after renaming 'id' to 'player_id': {combined_df.columns.tolist()}")
    else:
        logging.error("'id' column not found in the merged dataset.")
        return None

    # Ensure required columns exist
    required_columns = ['web_name', 'assists', 'yellow_cards', 'red_cards']
    for col in required_columns:
        if col not in combined_df.columns:
            combined_df[col] = None

    return combined_df

def integrate_data():
    fpl_players_path = 'data/fpl_players.csv'
    fpl_teams_path = 'data/fpl_teams.csv'
    understat_path = 'data/understat_players.csv'
    fpl_fixtures_path = 'data/fpl_fixtures.csv'

    fpl_players = load_csv(fpl_players_path)
    fpl_teams = load_csv(fpl_teams_path)
    understat_df = load_csv(understat_path)
    fpl_fixtures = load_csv(fpl_fixtures_path) if fpl_fixtures_path else None

    if fpl_players is not None and fpl_teams is not None and understat_df is not None:
        combined_df = merge_datasets(fpl_players, fpl_teams, understat_df, fpl_fixtures)
        if combined_df is not None:
            if 'player_id' in combined_df.columns:
                combined_df.drop_duplicates(subset='player_id', inplace=True)
                combined_df.to_csv('data/enhanced_fpl_players.csv', index=False)
                logging.info("Data saved to data/enhanced_fpl_players.csv")
                logging.info(f"First few rows of the combined dataset:\n{combined_df.head()}")
            else:
                logging.error("'player_id' column not found in the combined dataset.")
        else:
            logging.error("Merging datasets failed.")
    else:
        logging.error("Failed to load one or more input files. Cannot proceed with merging datasets.")

if __name__ == "__main__":
    integrate_data()
