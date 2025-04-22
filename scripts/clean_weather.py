import json
import pandas as pd 

def clean_weather():
    with open("/Users/luisl/OneDrive/Documents/LUIS/Project/YourProjectName/DEPath2/weather_etl/data/raw_weather.json", "r") as f:
        data=json.load(f)

    cleaned = {
        "location": data["location"]["name"],
        "temp_c":data["current"]["temp_c"],
        "condition": data["current"]["condition"]["text"],
        "timestamp": data["location"]["localtime"]
    }

    df = pd.DataFrame([cleaned])
    df.to_csv("/Users/luisl/OneDrive/Documents/LUIS/Project/YourProjectName/DEPath2/weather_etl/data/cleaned_weather.csv", index=False)