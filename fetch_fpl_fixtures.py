import requests
import pandas as pd

def fetch_latest_fixtures():
    url = 'https://fantasy.premierleague.com/api/fixtures/'
    response = requests.get(url)
    if response.status_code == 200:
        fixtures = response.json()
        fixtures_df = pd.DataFrame(fixtures)
        fixtures_df.to_csv('data/latest_fpl_fixtures.csv', index=False)
        print("Latest fixtures data saved to data/latest_fpl_fixtures.csv")
    else:
        print(f"Failed to fetch fixtures data: {response.status_code}")

fetch_latest_fixtures()
