import requests
import pandas as pd

def fetch_fpl_data():
    fpl_url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    fpl_response = requests.get(fpl_url)
    fpl_data = fpl_response.json()
    
    # Players data
    elements_df = pd.DataFrame(fpl_data['elements'])
    elements_df.to_csv('data/fpl_players.csv', index=False)
    
    # Teams data
    teams_df = pd.DataFrame(fpl_data['teams'])
    teams_df.to_csv('data/fpl_teams.csv', index=False)

    # Fixtures data
    fixtures_url = 'https://fantasy.premierleague.com/api/fixtures/'
    fixtures_response = requests.get(fixtures_url)
    fixtures_data = fixtures_response.json()
    fixtures_df = pd.DataFrame(fixtures_data)
    fixtures_df.to_csv('data/fpl_fixtures.csv', index=False)

fetch_fpl_data()
