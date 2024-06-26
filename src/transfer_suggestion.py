import pandas as pd

def suggest_transfers(current_squad, available_budget, model, data, free_transfers):
    try:
        # Ensure the features are in the correct order
        feature_columns = [
            'minutes', 'goals_scored', 'assists', 'clean_sheets', 'goals_conceded',
            'own_goals', 'penalties_saved', 'penalties_missed', 'yellow_cards',
            'red_cards', 'saves', 'bonus', 'bps', 'influence', 'creativity', 'threat',
            'ict_index', 'starts', 'expected_goals', 'expected_assists',
            'expected_goal_involvements', 'expected_goals_conceded', 'form', 'now_cost'
        ]

        # Ensure 'player_id' and 'web_name' are in the data
        if 'player_id' not in data.columns or 'web_name' not in data.columns:
            raise ValueError("'player_id' or 'web_name' column is missing from the data")

        # Create a dictionary to map team IDs to team names
        team_mapping = data[['team', 'team_name']].drop_duplicates().set_index('team')['team_name'].to_dict()

        # Predict the expected points for all players
        predicted_points = model.predict(data[feature_columns])
        data['expected_points'] = predicted_points

        # Calculate current team's expected points
        current_squad['expected_points'] = current_squad['player_id'].map(data.set_index('player_id')['expected_points'])
        current_team_points = current_squad['expected_points'].sum()

        # Sort players by expected points
        data = data.sort_values(by='expected_points', ascending=False)

        # Filter out current squad players
        current_ids = current_squad['player_id'].tolist()
        available_players = data[~data['player_id'].isin(current_ids)]

        best_suggestions = []
        best_reasons = []
        best_expected_points = current_team_points

        # Iterate over possible transfers from 1 to the number of free transfers + additional paid transfers
        for num_transfers in range(1, free_transfers + 3):  # Considering up to 3 additional transfers
            suggestions = []
            reasons = []
            remaining_budget = available_budget
            new_team_points = current_team_points
            for index, row in available_players.iterrows():
                if len(suggestions) >= num_transfers:
                    break
                out_player = current_squad.iloc[index % len(current_squad)]
                in_player = row

                out_price_str = out_player['Current price (£)'].strip('£m')
                try:
                    out_price = float(out_price_str)
                except ValueError:
                    print(f"Error converting price: {out_price_str}")
                    continue

                in_price = in_player['now_cost'] / 10  # Adjust as necessary

                if in_price <= out_price + remaining_budget:
                    suggestion = {
                        'Player Out': out_player['Player'],
                        'Out Team': out_player['team'],
                        'Player In': in_player['web_name'],
                        'In Team': team_mapping[in_player['team']],
                        'Remaining Budget': f"£{remaining_budget - (in_price - out_price):.1f}m"
                    }
                    suggestions.append(suggestion)
                    remaining_budget -= (in_price - out_price)
                    new_team_points += in_player['expected_points'] - out_player['expected_points']

                    # Calculate the points cost for additional transfers
                    points_cost = max(0, (num_transfers - free_transfers) * -4)
                    
                    # Construct the reason for the transfer suggestion
                    reason = (
                        f"{in_player['web_name']} is suggested as a transfer in because they are expected to score "
                        f"{in_player['expected_points']:.2f} points over the next 5 gameweeks. "
                        f"Historically, {in_player['web_name']} has shown strong performance with a form rating of "
                        f"{in_player['form']}. Additionally, their upcoming fixtures are favorable with a difficulty "
                        f"rating of {in_player['fixture_difficulty']}. Compared to other potential transfers, {in_player['web_name']} "
                        f"offers a better expected points return and fits within the budget constraints. This transfer would cost "
                        f"{points_cost} points due to the need for additional transfers."
                    )
                    reasons.append(reason)

            if new_team_points - points_cost > best_expected_points:
                best_expected_points = new_team_points - points_cost
                best_suggestions = suggestions
                best_reasons = reasons

        suggestions_df = pd.DataFrame(best_suggestions)
        reasons_df = pd.DataFrame(best_reasons, columns=['Reason'])
        return suggestions_df, reasons_df
    except Exception as e:
        print(f"Error in generating transfer suggestions: {e}")
        return pd.DataFrame(), pd.DataFrame()
