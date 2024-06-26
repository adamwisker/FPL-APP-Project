import requests
import pandas as pd
import json
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

def fetch_fpl_fixtures():
    fpl_fixtures_url = 'https://fantasy.premierleague.com/api/fixtures/'
    response = requests.get(fpl_fixtures_url)
    if response.status_code == 200:
        fixtures = response.json()
        fixtures_df = pd.DataFrame(fixtures)
        fixtures_df.to_csv('data/fpl_fixtures.csv', index=False)
        logging.info("Fixtures data saved to data/fpl_fixtures.csv")
    else:
        logging.error(f"Failed to fetch FPL fixtures data: {response.status_code}")

def fetch_understat_data():
    understat_url = 'https://understat.com/league/EPL'
    understat_response = requests.get(understat_url)
    soup = BeautifulSoup(understat_response.content, 'html.parser')
    scripts = soup.find_all('script')
    string_with_json_data = ''
    for script in scripts:
        if 'playersData' in script.text:
            string_with_json_data = script.text
            break

    start_index = string_with_json_data.index("('") + 2
    end_index = string_with_json_data.index("')")
    json_data = string_with_json_data[start_index:end_index].encode('utf8').decode('unicode_escape')
    
    try:
        parsed_data = json.loads(json_data)
        players_data = parsed_data
        understat_df = pd.DataFrame(players_data)
        understat_df.to_csv('data/understat_players.csv', index=False)
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON from Understat response")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_fpl_data()
    fetch_fpl_fixtures()
    fetch_understat_data()
