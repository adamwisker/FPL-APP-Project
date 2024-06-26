import requests
import pandas as pd
import json
from bs4 import BeautifulSoup

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
        print("Failed to decode JSON from Understat response")
    except Exception as e:
        print(f"An error occurred: {e}")

fetch_understat_data()
