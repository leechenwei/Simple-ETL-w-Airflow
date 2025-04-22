<h2>🌤️ Simple Weather ETL with Airflow</h2>

This is a beginner-friendly ETL project built to get hands-on experience with Apache Airflow. The pipeline simulates a weather data ETL process — without using any APIs. Instead, the data is manually prepared, then processed step-by-step:<br>

Fetch data (read from local)<br>

Clean data (basic transformation)<br>

Load to PostgreSQL (via Docker)<br>

<h2>🚀 Project Overview</h2>

Built to understand Airflow DAGs and task dependencies.<br>

Mimics a real-world ETL pipeline, but in a simple and controlled way.<br>

PostgreSQL is used as the data warehouse, running inside Docker.<br>

<h2>📋 Prerequisites</h2>
1.Python (3.8+ recommended)<br>

2.Apache Airflow<br> <tab><b>pip install apache-airflow</b></tab><br>

3.Docker (for running PostgreSQL)<br>

<h2>🔧 Setup</h2>
1.Start PostgreSQL via Docker<br>

2.Set up Airflow (you can use the default setup or follow Airflow's docs).<br>

3.Trigger the DAG that runs:<br>

fetch_weather_data<br>

clean_weather_data<br>

load_to_postgres<br>

