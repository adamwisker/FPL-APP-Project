import os
import pandas as pd
import requests

# Step 1: Get Player Data
def fetch_player_data():
    # URL of the player data
    player_data_url = 'https://fantasy.premierleague.com/api/bootstrap-static/'

    # Fetch the player data
    response = requests.get(player_data_url)
    data = response.json()

    # Convert player data to DataFrame
    players_df = pd.DataFrame(data['elements'])

    # Extract player ID, name, and code
    player_info = players_df[['id', 'web_name', 'code']]

    return player_info

# Step 2: Download Player Images
def download_player_images(player_info):
    # Directory to save images
    os.makedirs('player_images', exist_ok=True)

    # Base URL for player images
    base_image_url = 'https://resources.premierleague.com/premierleague/photos/players/110x140/'

    # Loop through each player and download the image
    for idx, row in player_info.iterrows():
        player_code = row['code']
        player_name = row['web_name']
        image_url = f'{base_image_url}p{player_code}.png'
        image_path = os.path.join('player_images', f'{player_name}.png')

        try:
            img_response = requests.get(image_url, headers={'User-Agent': 'Mozilla/5.0'})
            img_response.raise_for_status()  # Check if the request was successful
            with open(image_path, 'wb') as img_file:
                img_file.write(img_response.content)
            print(f"Downloaded {player_name}'s image.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download image for {player_name}: {e}")

    print("All images downloaded successfully.")

if __name__ == "__main__":
    player_info = fetch_player_data()
    download_player_images(player_info)
