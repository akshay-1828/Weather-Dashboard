import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

CITIES = ["Bangalore", "Mumbai", "Delhi"]
CSV_FILE = "weather_data.csv"

def generate_mock_data():
    """Generates 7 days of historical weather data for testing the dashboard."""
    records = []
    end_time = datetime.now()
    start_time = end_time - timedelta(days=7)
    
    current_time = start_time
    
    # Base temperatures and logic for mock data
    bases = {
        "Bangalore": {"temp": 28, "hum": 65},
        "Mumbai": {"temp": 32, "hum": 80},
        "Delhi": {"temp": 35, "hum": 55}
    }
    
    while current_time <= end_time:
        for city in CITIES:
            # Add some diurnal variation using a sine wave based on hour
            hour = current_time.hour
            # Peak temp around 2 PM (14:00), lowest around 4 AM (04:00)
            time_offset = (hour - 14) / 24 * 2 * np.pi
            diurnal_variation = np.cos(time_offset) * 5 
            
            temp = bases[city]["temp"] + diurnal_variation + random.uniform(-2, 2)
            hum = bases[city]["hum"] - diurnal_variation*1.5 + random.uniform(-5, 5) # Humidity tends to be inverse to temp
            
            # Clamp humidity to 0-100
            hum = max(0, min(100, hum))
            
            conditions = ["Clear", "Clouds", "Rain", "Haze"]
            weights = [0.4, 0.4, 0.1, 0.1]
            condition = random.choices(conditions, weights=weights)[0]
            
            records.append({
                "Timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "City": city,
                "Temperature (C)": round(temp, 2),
                "Humidity (%)": round(hum, 1),
                "Weather Condition": condition
            })
            
        # 1-hour intervals for mock data
        current_time += timedelta(hours=1)
        
    df = pd.DataFrame(records)
    df.to_csv(CSV_FILE, index=False)
    print(f"Generated {len(df)} rows of mock data in {CSV_FILE}.")

if __name__ == "__main__":
    generate_mock_data()
