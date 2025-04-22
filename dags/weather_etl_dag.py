from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import sys
import json
import logging
import pandas as pd
import psycopg2

# Default arguments for DAG
default_args = {
    'owner': 'you',
    'start_date': datetime(2025, 4, 21),
    'retries': 0
}

sys.path.insert(0, os.path.abspath('/Users/luisl/airflow/scripts'))

# Set up basic logging configuration
logging.basicConfig(
    level=logging.INFO,  # This can be adjusted to DEBUG or ERROR based on your needs
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Function to manually create raw weather data
def fetch_weather():
    logging.info("Starting the fetch_weather function.")
    
    # Simulated raw weather data (you can replace this with any other weather data structure you need)
    weather_data = {
        "location": {
            "name": "Singapore",
            "region": "",
            "country": "Singapore",
            "lat": 1.3521,
            "lon": 103.8198,
            "tz_id": "Asia/Singapore",
            "localtime_epoch": 1626801600,
            "localtime": "2021-07-21 12:00"
        },
        "current": {
            "temp_c": 30.5,
            "temp_f": 87.3,
            "is_day": 1,
            "condition": {
                "text": "Clear",
                "icon": "//cdn.weatherapi.com/weather/64x64/day/113.png",
                "code": 1000
            },
            "humidity": 70,
            "precip_mm": 0.0,
            "precip_in": 0.0,
            "pressure_mb": 1010.0,
            "pressure_in": 29.83,
            "wind_kph": 15.0,
            "wind_degree": 90,
            "wind_dir": "E",
            "cloud": 0,
            "feelslike_c": 32.0,
            "feelslike_f": 89.6,
            "vis_km": 10.0,
            "vis_miles": 6.0,
            "uv": 7.0,
            "gust_kph": 18.0,
            "gust_mph": 11.2
        }
    }

    try:
        # Save the simulated raw weather data to a JSON file
        with open("raw_weather.json", "w") as f:
            json.dump(weather_data, f)
        
        logging.info("Weather data manually created and saved successfully.")
    
    except Exception as e:
        logging.error(f"An error occurred while creating the weather data: {e}")

# Function to clean weather data
def clean_weather():
    logging.info("Starting the clean_weather function.")
    
    try:
        with open("raw_weather.json", "r") as f:
            data = json.load(f)
        
        # Ensure that the data is in the expected dictionary format
        if isinstance(data, dict) and "location" in data and "current" in data:
            # Example cleaning step: extracting only needed data
            cleaned_data = {
                "location": data["location"]["name"],
                "temperature": data["current"]["temp_c"],
                "condition": data["current"]["condition"]["text"],
                "timestamp": datetime.now()  # Add timestamp for when the data was fetched
            }

            # Save the cleaned data to a CSV file
            df = pd.DataFrame([cleaned_data])
            df.to_csv("cleaned_weather.csv", index=False)
            
            logging.info("Weather data cleaned and saved successfully.")
        else:
            logging.error("Data format is incorrect. Please check the raw weather data.")

    except Exception as e:
        logging.error(f"An error occurred during cleaning: {e}")

# Function to load weather data to Postgres
def load_to_postgres():
    logging.info("Starting the load_to_postgres function.")
    
    try:
        # Read the cleaned data from the CSV file
        df = pd.read_csv("cleaned_weather.csv")

        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname="weather_db",
            user="airflow_user",
            password="airflow_pass",
            host="localhost",
            port="5432"
        )

        cur = conn.cursor()

        # Create the weather_data table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS weather_data (
                location TEXT,
                temperature FLOAT,
                condition TEXT,
                timestamp TIMESTAMP
            );
        """)
        logging.info("Table 'weather_data' ensured to exist.")
        
        # Insert data into the table
        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO weather_data (location, temperature, condition, timestamp)
                VALUES (%s, %s, %s, %s)
            """, (row['location'], row['temperature'], row['condition'], row['timestamp']))

        conn.commit()
        logging.info("Weather data loaded into PostgreSQL successfully.")
    
    except psycopg2.Error as e:
        logging.error(f"PostgreSQL error: {e}")
    
    except Exception as e:
        logging.error(f"An error occurred while loading to PostgreSQL: {e}")
    
    finally:
        # Close connections
        if conn:
            cur.close()
            conn.close()

# Define the DAG
with DAG("weather_etl",
         default_args=default_args,
         schedule_interval="@daily",
         catchup=False) as dag:

    # Define the tasks
    t1 = PythonOperator(
        task_id='fetch_weather',
        python_callable=fetch_weather
    )

    t2 = PythonOperator(
        task_id='clean_weather',
        python_callable=clean_weather
    )

    t3 = PythonOperator(
        task_id='load_to_postgres',
        python_callable=load_to_postgres
    )

    # Set the task dependencies
    t1 >> t2 >> t3
