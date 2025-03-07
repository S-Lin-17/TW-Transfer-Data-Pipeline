import os
from datetime import datetime, timedelta
import psycopg2
import subprocess

import secrets
import download_data
import insert_data
import validate
    
def main():  

    try:
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
        print("Requirements installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        return

    # # Create local db if it doesn't exist
    try:
        subprocess.run(["bash", "./create_db.sh"], check=True)
        print("Database setup completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error setting up database: {e}")
        return 1
    
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
                    csv_content = download_data.download_csv(gas_day, cycle)
                    cycle_date = f"{gas_day.strftime('%Y%m%d')}_cycle-{cycles[cycle]}"
                    
                    # Save csv file in data folder (for testing)
                    # file_name = cycle_date + ".csv"
                    # os.makedirs("data", exist_ok=True)
                    # file_path = os.path.join("data", file_name)
                    # with open(file_path, "wb") as f:
                    #     f.write(csv_content)
                    
                    # Validate data
                    df = validate.validate_data(csv_content, cycle_date)
                    
                    # Add gas day and cycle columns
                    df["Gas Day"] = gas_day
                    df["Cycle"] = cycle

                    cursor = insert_data(df, connection)

                    if df is not None: 
                        print(f"Data is valid")

                except Exception as e:
                    print(f"Error processing {gas_day}, cycle {cycle}: {e}")

    except Exception as e:
        print(f"An error occurred connecting with the database: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()