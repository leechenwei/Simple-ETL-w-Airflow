import psycopg2
import pandas as pd 

def load_to_postgres():
    df=pd.read_csv("/Users/luisl/OneDrive/Documents/LUIS/Project/YourProjectName/DEPath2/weather_etl/data/cleaned_weather.csv")

    conn = psycopg2.connect(
        dbname = "weather_db",
        user="airflow_user",
        password="airflow_pass",
        host="localhost",
        port="5432"
    )

    cur= conn.cursor()

    cur.execute("""
            CREATE TABLE IF NOT EXISTS weather_data (
                        location TEXT,
                        temp_c FLOAT,
                        condition TEXT,
                        timestamp TIMESTAMP
                );
                """)
    
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO weather_data (location, temp_c, condition, timestamp)
            VALUES (%s, %s, %s, %s)
        """, tuple(row))

    conn.commit()
    cur.close()
    conn.close()