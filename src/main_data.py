import os
import requests
from datetime import datetime, timedelta
import psycopg2

import validate
import secrets
import insert_data

BASE_URL = "https://twtransfer.energytransfer.com/ipost/TW/capacity/operationally-available"

def download_csv(gas_day, cycle):

    params = {
        "f": "csv",
        "extension": "csv",
        "asset": "TW",
        "gasDay": gas_day.strftime("%m/%d/%Y"),
        "cycle": cycle,
        "searchType": "NOM",
        "searchString": "",
        "locType": "ALL",
        "locZone": "ALL"
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to download CSV for {gas_day}, cycle {cycle}")
    
def main():    
    connection = None
    try:
        connection = psycopg2.connect(
            host=secrets.DB_HOST,
            database=secrets.DB_NAME,
            user=secrets.DB_USER,
            password=secrets.DB_PASSWORD
        )
        print("Connected to the database successfully!")

        today = datetime.today().date()

        cycles = {
            0: "Timely", 
            1: "Evening", 
            3: "Intraday 1", 
            4: "Intraday 2", 
            7: "Intraday 3", 
            5: "Final"
        }

        # Get data from last 3 days (excluding today)
        for i in range(1, 4):
            gas_day = today - timedelta(days=i)

            for cycle in cycles:
                try:
                    print(f"Processing data from cycle {cycles[cycle]} for {gas_day}")
                    csv_content = download_csv(gas_day, cycle)
                    cycle_date = f"{gas_day.strftime('%Y%m%d')}_cycle-{cycles[cycle]}"
                    
                    # Save csv file in data folder (TODO: delete after connection is created)
                    file_name = cycle_date + ".csv"
                    os.makedirs("data", exist_ok=True)
                    file_path = os.path.join("data", file_name)
                    with open(file_path, "wb") as f:
                        f.write(csv_content)
                    
                    # Validate data
                    df = validate.validate_data(csv_content, cycle_date)
                    
                    # Add gas day and cycle columns
                    df["Gas Day"] = gas_day
                    df["Cycle"] = cycle

                    insert_data(df, connection)

                    if df is not None: 
                        print(f"Data is valid")

                except Exception as e:
                    print(f"Error processing {gas_day}, cycle {cycle}: {e}")

    except Exception as e:
        print(f"An error occurred connecting with the database: {e}")
    finally:
        if connection:
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()