import streamlit as st
import pandas as pd
import joblib
from src.data_loader import load_data
from src.fetch_user_squad import fetch_user_squad
from src.transfer_suggestion import suggest_transfers

# Load the trained model
model = joblib.load('models/trained_model.pkl')

# Load data
data = load_data()

st.title('Fantasy Premier League AI Transfer Tool')

# Input for FPL user ID
user_id = st.text_input('Enter your FPL user ID:')
if user_id:
    try:
        user_id = int(user_id)
        
        # Fetch user squad details
        current_squad, team_name, team_value, free_transfers, available_budget = fetch_user_squad(user_id)
        
        if not current_squad.empty:
            # Display team information
            st.write(f"### {team_name}")
            st.write(f"**Team Value:** £{team_value:.1f}m")
            st.write(f"**Free Transfers:** {free_transfers}")
            st.write(f"**Available Budget:** £{available_budget:.1f}m")

            # Sort the squad into starting 11 and bench
            starting_11 = current_squad[current_squad['starting'] == True]
            bench = current_squad[current_squad['starting'] == False]

            # Sort by position: GK, DEF, MID, FWD
            position_order = {'GK': 0, 'DEF': 1, 'MID': 2, 'FWD': 3}
            starting_11 = starting_11.sort_values(by='position', key=lambda x: x.map(position_order))
            bench = bench.sort_values(by='position', key=lambda x: x.map(position_order))

            # Display the starting 11
            st.write('### Starting 11')
            st.table(starting_11[['Player', 'team', 'position', 'Current price (£)']].reset_index(drop=True))

            # Display the bench
            st.write('### Bench')
            st.table(bench[['Player', 'team', 'position', 'Current price (£)']].reset_index(drop=True))

            # Button to get transfer suggestions
            if st.button('Get Transfer Suggestions'):
                suggestions, reasons = suggest_transfers(current_squad, available_budget, model, data, free_transfers)
                if not suggestions.empty:
                    st.write("### Transfer Suggestions")
                    suggestions['Out Player Price (£m)'] = suggestions['Player Out'].apply(lambda x: current_squad[current_squad['Player'] == x]['Current price (£)'].values[0])
                    suggestions['In Player Price (£m)'] = suggestions['Player In'].apply(lambda x: data[data['web_name'] == x]['now_cost'].values[0] / 10)
                    
                    # Formatting the prices correctly
                    suggestions['Out Player Price (£m)'] = suggestions['Out Player Price (£m)'].apply(lambda x: f"£{float(x.replace('£', '').replace('m', ''))}m")
                    suggestions['In Player Price (£m)'] = suggestions['In Player Price (£m)'].apply(lambda x: f"£{x:.1f}m")
                    
                    st.table(suggestions[['Player Out', 'Out Team', 'Out Player Price (£m)', 'Player In', 'In Team', 'In Player Price (£m)', 'Remaining Budget']])
                    
                    st.write("### Reasons for Suggestions")
                    for reason in reasons['Reason']:
                        st.write(reason)
                else:
                    st.write("No suitable transfers found within the available budget.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
