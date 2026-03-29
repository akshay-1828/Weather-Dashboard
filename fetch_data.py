import requests
import pandas as pd
import time
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv('OPENWEATHER_API_KEY')
CITIES = ["Bangalore", "Mumbai", "Delhi"]
CSV_FILE = "weather_data.csv"
FETCH_INTERVAL_SECONDS = 600  # 10 minutes

def get_weather(city):
    """Fetches real-time weather data for a given city using OpenWeather API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "City": city,
            "Temperature (C)": data["main"]["temp"],
            "Humidity (%)": data["main"]["humidity"],
            "Weather Condition": data["weather"][0]["main"]
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {city}: {e}")
        return None

def main():
    if not API_KEY or API_KEY == "your_api_key_here":
        print("WARNING: Please set your OPENWEATHER_API_KEY in the .env file")
        print("The fetcher will not work without a valid API key.")
        return

    print("Starting Real-Time Weather Data Fetcher...")
    while True:
        records = []
        for city in CITIES:
            data = get_weather(city)
            if data:
                records.append(data)
        
        if records:
            df = pd.DataFrame(records)
            mode = 'a' if os.path.exists(CSV_FILE) else 'w'
            header = not os.path.exists(CSV_FILE)
            
            # Save to CSV
            df.to_csv(CSV_FILE, mode=mode, header=header, index=False)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Appended {len(records)} records to {CSV_FILE}")
            
        print(f"Waiting {FETCH_INTERVAL_SECONDS} seconds before the next fetch...")
        time.sleep(FETCH_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
