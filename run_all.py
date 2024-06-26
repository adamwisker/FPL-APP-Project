import logging
from fetch_data import fetch_fpl_data, fetch_fpl_fixtures, fetch_understat_data
from integrate_data import integrate_data
from train_model import train_model

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        # Step 1: Fetch FPL and Understat data
        logging.info("Fetching FPL and Understat data...")
        fetch_fpl_data()
        fetch_fpl_fixtures()
        fetch_understat_data()
        
        # Step 2: Integrate data
        logging.info("Integrating data...")
        integrate_data()
        
        # Step 3: Train the model
        logging.info("Training the model...")
        train_model()
        
        logging.info("All steps completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
