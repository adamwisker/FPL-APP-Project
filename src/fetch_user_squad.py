import requests
import pandas as pd

def fetch_user_squad(user_id):
    try:
        # Fetch user team details
        team_url = f"https://fantasy.premierleague.com/api/entry/{user_id}/"
        team_response = requests.get(team_url)
        team_response.raise_for_status()
        team_data = team_response.json()
        
        # Fetch history details
        history_url = f"https://fantasy.premierleague.com/api/entry/{user_id}/history/"
        history_response = requests.get(history_url)
        history_response.raise_for_status()
        history_data = history_response.json()

        # Get the latest event ID
        current_event_id = max(history_data['current'], key=lambda x: x['event'])['event']

        # Fetch picks details for the current event
        picks_url = f"https://fantasy.premierleague.com/api/entry/{user_id}/event/{current_event_id}/picks/"
        picks_response = requests.get(picks_url)
        picks_response.raise_for_status()
        picks_data = picks_response.json()

        # Fetch general player data
        player_url = "https://fantasy.premierleague.com/api/bootstrap-static/"
        player_response = requests.get(player_url)
        player_response.raise_for_status()
        player_data = player_response.json()
        players_df = pd.DataFrame(player_data['elements'])

        # Fetch team names
        teams_df = pd.DataFrame(player_data['teams'])

        # Extract relevant information
        team_name = team_data['name']
        team_value = team_data['last_deadline_value'] / 10  # Example conversion
        available_budget = team_data['last_deadline_bank'] / 10  # Example conversion
        free_transfers = history_data['current'][-1].get('event_transfers', 1)

        # Get player's squad details
        picks = picks_data['picks']
        player_ids = [pick['element'] for pick in picks]

        squad_df = players_df[players_df['id'].isin(player_ids)].copy()
        squad_df['Current price (£)'] = squad_df['now_cost'] / 10
        squad_df['Current price (£)'] = squad_df['Current price (£)'].apply(lambda x: f"£{x:.1f}m")
        squad_df['team'] = squad_df['team'].map(teams_df.set_index('id')['name'])
        squad_df = squad_df[['web_name', 'team', 'element_type', 'Current price (£)', 'id']]

        # Map position types
        position_map = {1: 'GK', 2: 'DEF', 3: 'MID', 4: 'FWD'}
        squad_df['position'] = squad_df['element_type'].map(position_map)
        squad_df.rename(columns={'web_name': 'Player', 'id': 'player_id'}, inplace=True)

        # Identify starting 11 and bench
        for pick in picks:
            player_id = pick['element']
            is_starting = pick['position'] <= 11
            squad_df.loc[squad_df['player_id'] == player_id, 'starting'] = is_starting

        return squad_df, team_name, team_value, free_transfers, available_budget
    except requests.exceptions.HTTPError as http_err:
        raise ValueError(f"HTTP error occurred: {http_err}")
    except KeyError as key_err:
        raise ValueError(f"Error fetching data: {key_err}")
    except Exception as err:
        raise ValueError(f"An error occurred: {err}")
