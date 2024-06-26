import pandas as pd

def load_data():
    data_path = 'data/enhanced_fpl_players.csv'

    # Load the data without specifying data types first
    data = pd.read_csv(data_path, low_memory=False)

    # Fill NA values appropriately
    bool_columns = ['in_dreamteam', 'special']
    for col in bool_columns:
        if col in data.columns:
            data[col] = data[col].fillna(False)

    int_columns = data.select_dtypes(include=['int64', 'float64']).columns
    for col in int_columns:
        data[col] = data[col].fillna(0)

    # Cast columns to the appropriate data types
    dtype_spec = {
        'chance_of_playing_next_round': 'float64',
        'chance_of_playing_this_round': 'float64',
        'code': 'int64',
        'cost_change_event': 'int64',
        'cost_change_event_fall': 'int64',
        'cost_change_start': 'int64',
        'cost_change_start_fall': 'int64',
        'dreamteam_count': 'int64',
        'element_type': 'int64',
        'ep_next': 'float64',
        'ep_this': 'float64',
        'event_points': 'int64',
        'first_name': 'str',
        'form': 'float64',
        'id': 'int64',
        'in_dreamteam': 'bool',
        'news': 'str',
        'news_added': 'str',
        'now_cost': 'int64',
        'photo': 'str',
        'points_per_game': 'float64',
        'second_name': 'str',
        'selected_by_percent': 'float64',
        'special': 'bool',
        'squad_number': 'str',
        'status': 'str',
        'team': 'int64',
        'team_code': 'int64',
        'total_points': 'int64',
        'transfers_in': 'int64',
        'transfers_in_event': 'int64',
        'transfers_out': 'int64',
        'transfers_out_event': 'int64',
        'value_form': 'float64',
        'value_season': 'float64',
        'web_name': 'str',
        'minutes': 'int64',
        'goals_scored': 'int64',
        'assists': 'int64',
        'clean_sheets': 'int64',
        'goals_conceded': 'int64',
        'own_goals': 'int64',
        'penalties_saved': 'int64',
        'penalties_missed': 'int64',
        'yellow_cards': 'int64',
        'red_cards': 'int64',
        'saves': 'int64',
        'bonus': 'int64',
        'bps': 'int64',
        'influence': 'float64',
        'creativity': 'float64',
        'threat': 'float64',
        'ict_index': 'float64',
        'starts': 'int64',
        'expected_goals': 'float64',
        'expected_assists': 'float64',
        'expected_goal_involvements': 'float64',
        'expected_goals_conceded': 'float64',
        'influence_rank': 'int64',
        'influence_rank_type': 'int64',
        'creativity_rank': 'int64',
        'creativity_rank_type': 'int64',
        'threat_rank': 'int64',
        'threat_rank_type': 'int64',
        'ict_index_rank': 'int64',
        'ict_index_rank_type': 'int64',
        'corners_and_indirect_freekicks_order': 'str',
        'corners_and_indirect_freekicks_text': 'str',
        'direct_freekicks_order': 'str',
        'direct_freekicks_text': 'str',
        'penalties_order': 'str',
        'penalties_text': 'str',
        'expected_goals_per_90': 'float64',
        'saves_per_90': 'float64',
        'expected_assists_per_90': 'float64',
        'expected_goal_involvements_per_90': 'float64',
        'expected_goals_conceded_per_90': 'float64',
        'goals_conceded_per_90': 'float64',
        'now_cost_rank': 'int64',
        'now_cost_rank_type': 'int64',
        'form_rank': 'int64',
        'form_rank_type': 'int64',
        'points_per_game_rank': 'int64',
        'points_per_game_rank_type': 'int64',
        'selected_rank': 'int64',
        'selected_rank_type': 'int64',
        'starts_per_90': 'float64',
        'clean_sheets_per_90': 'float64',
        'fixture_difficulty': 'float64'
    }

    for column, dtype in dtype_spec.items():
        if column in data.columns:
            data[column] = data[column].astype(dtype)

    # Add team names mapping for the 2024/25 season
    team_names = {
        1: 'Arsenal', 2: 'Aston Villa', 3: 'Bournemouth', 4: 'Brentford', 5: 'Brighton & Hove Albion',
        6: 'Chelsea', 7: 'Crystal Palace', 8: 'Everton', 9: 'Fulham', 10: 'Ipswich Town',
        11: 'Leicester City', 12: 'Liverpool', 13: 'Manchester City', 14: 'Manchester United', 15: 'Newcastle United',
        16: 'Nottingham Forest', 17: 'Southampton', 18: 'Tottenham Hotspur', 19: 'West Ham United', 20: 'Wolverhampton Wanderers'
    }

    data['team_name'] = data['team'].map(team_names)

    # Add any missing expected columns with default values
    required_columns = ['assists', 'yellow_cards', 'red_cards', 'games', 'key_passes', 'npg', 'npxG', 'shots', 'time', 'xG', 'xA', 'xGChain', 'xGBuildup']
    for col in required_columns:
        if col not in data.columns:
            data[col] = 0

    # Ensure necessary columns for transfer suggestion are present
    required_columns_for_suggestion = [
        'player_id', 'web_name', 'team', 'team_name', 'now_cost', 'minutes', 'goals_scored', 'assists',
        'clean_sheets', 'goals_conceded', 'own_goals', 'penalties_saved', 'penalties_missed',
        'yellow_cards', 'red_cards', 'saves', 'bonus', 'bps', 'influence', 'creativity', 'threat',
        'ict_index', 'starts', 'expected_goals', 'expected_assists', 'expected_goal_involvements',
        'expected_goals_conceded', 'form', 'fixture_difficulty'
    ]
    
    # If fixture_difficulty is not present, calculate or set default
    if 'fixture_difficulty' not in data.columns:
        data['fixture_difficulty'] = 3.0  # Set a default value or calculate based on your logic

    missing_columns = [col for col in required_columns_for_suggestion if col not in data.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    return data
