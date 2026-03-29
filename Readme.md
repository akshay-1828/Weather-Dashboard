🌦 Real-Time Multi-City Weather Analytics & Prediction Dashboard
🚀 Overview

This project is a real-time data analytics dashboard that fetches live weather data using an API, stores historical data, performs analysis, and visualizes trends with predictions.

It demonstrates an end-to-end data analysis workflow including:

Data collection (API)
Data storage
Data analysis
Data visualization
Basic Machine Learning
🎯 Features
🌐 Real-time weather data using OpenWeather API
🏙 Multi-city support (Bangalore, Mumbai, Delhi)
📊 Interactive dashboard using Streamlit
📈 Temperature & humidity trend visualization
📉 Historical data tracking
🚨 Smart alerts (high temperature / humidity)
🤖 Temperature prediction using Linear Regression
🎨 Clean and user-friendly UI
🛠 Tech Stack
Python
Pandas
Matplotlib
Streamlit
Requests (API calls)
Scikit-learn (Machine Learning)
📁 Project Structure
weather_project/
│
├── fetch_data.py        # Fetches real-time weather data
├── app.py               # Streamlit dashboard
├── weather_data.csv     # Stored historical data
├── requirements.txt     # Dependencies
└── README.md
⚙️ Setup Instructions
1️⃣ Clone the repository
git clone https://github.com/your-username/weather-dashboard.git
cd weather-dashboard
2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Add your API key

Get your API key from OpenWeather and update in fetch_data.py:

API_KEY = "your_api_key_here"
4️⃣ Run data collection script
python fetch_data.py

Run multiple times to build dataset.

5️⃣ Run dashboard
streamlit run app.py
📊 Example Insights
High temperature trends observed during daytime
Humidity increases when temperature drops
Certain cities show higher fluctuations
🤖 Machine Learning
Implemented Linear Regression to predict future temperature
Helps in understanding upcoming trends
💡 Future Improvements
Auto data collection using scheduler
Deploy dashboard online
Add more weather parameters (wind, pressure)
Use advanced ML models
