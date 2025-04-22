import requests
import json
import logging

# Set up basic logging configuration
logging.basicConfig(
    level=logging.DEBUG,  # Adjusted to DEBUG for more detailed logs
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def fetch_weather():
    logging.info("Starting the fetch_weather function.")
    
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": "2d400348a10b463586852804252104",  # Replace with your actual API key
        "q": "Singapore",
        "aqi": "no"
    }
    
    logging.debug(f"Prepared API request to {url} with parameters: {params}")
    
    try:
        logging.info(f"Sending request to {url} with params {params}")
        response = requests.get(url, params=params, timeout=30)  # 30-second timeout
        
        # Log the response status code and text
        logging.info(f"Received response with status code: {response.status_code}")
        logging.debug(f"Response Text: {response.text}")
        
        # Check if the response is successful
        response.raise_for_status()  # This will raise an exception for any 4xx or 5xx status codes
        
        # Log the JSON data returned
        data = response.json()
        logging.debug(f"Response JSON: {json.dumps(data, indent=4)}")
        
        logging.info("Weather data fetched successfully.")
        
        # Save the fetched data to a file
        with open("cleaned_weather.json", "w") as f:
            json.dump(data, f)
        logging.info("Weather data saved successfully.")

    except requests.exceptions.Timeout:
        logging.error("The request timed out.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

