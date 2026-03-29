import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np
import os
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# ==========================================
# Page Configuration
# ==========================================
st.set_page_config(
    page_title="Weather Analytics Dashboard",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling aesthetics
st.markdown("""
<style>
    .kpi-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        border-left: 5px solid #0056b3;
    }
    .kpi-title { font-size: 1.2rem; font-weight: bold; color: #333; }
    .kpi-value { font-size: 2rem; font-weight: bold; color: #0056b3; }
</style>
""", unsafe_allow_html=True)

DATA_FILE = "weather_data.csv"

# ==========================================
# Auto-refresh Configuration
# ==========================================
# Auto-refresh every 60 seconds (60000 milliseconds)
count = st_autorefresh(interval=60000, key="weather_dashboard_autorefresh")

# ==========================================
# Data Loading
# ==========================================
@st.cache_data(ttl=30)
def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame()
    df = pd.read_csv(DATA_FILE)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df.sort_values('Timestamp')
    return df

df = load_data()

# ==========================================
# Application Header
# ==========================================
st.title("🌤️ Real-Time Multi-City Weather Analytics Dashboard")
st.markdown("A dynamic data platform fetching real-time weather KPIs, visualizing trends across cities, alerting on critical conditions, and forecasting near-future temperatures utilizing **Machine Learning**.")
st.markdown("---")

if df.empty:
    st.warning("No data found! Please ensure `fetch_data.py` has run at least once.")
    st.info("Tip: You can generate dummy data by running `python generate_mock_data.py`.")
    st.stop()

city_list = df['City'].unique()

# ==========================================
# Sidebar Configuration
# ==========================================
with st.sidebar:
    st.header("⚙️ Configuration")
    selected_city = st.selectbox("Select City for ML & Deep Analysis", city_list)
    
    st.markdown("---")
    st.markdown("**Overview:**")
    st.markdown("- Real-time API Integration")
    st.markdown("- Auto-refresh enabled")
    st.markdown("- Predictive ML models")
    
    st.markdown("---")
    if st.button("🔄 Manual Refresh"):
        st.cache_data.clear()
        st.rerun()

# ==========================================
# Latest KPI Cards section
# ==========================================
st.header("📊 Latest Weather KPIs")
latest_data = df.groupby('City').last().reset_index()

# We will display columns dynamically based on the number of cities
cols = st.columns(len(city_list))
for i, city in enumerate(city_list):
    city_data = latest_data[latest_data['City'] == city].iloc[0]
    with cols[i]:
        # Using native metric, but we can style if needed
        st.metric(
            label=f"🌡️ {city} Temperature",
            value=f"{city_data['Temperature (C)']} °C",
            delta=city_data['Weather Condition']
        )
        st.metric(
            label=f"💧 {city} Humidity",
            value=f"{city_data['Humidity (%)']}%"
        )
        
# ==========================================
# Alerts System
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("🚨 Live Alert System")
alert_cols = st.columns(len(city_list))
for i, city in enumerate(city_list):
    city_data = latest_data[latest_data['City'] == city].iloc[0]
    temp = city_data['Temperature (C)']
    hum = city_data['Humidity (%)']
    
    with alert_cols[i]:
        warning_shown = False
        if temp > 35:
            st.error(f"High Temp Alert: {temp}°C in {city}!")
            warning_shown = True
        elif temp < 10:
            st.info(f"Low Temp Alert: {temp}°C in {city}!")
            warning_shown = True
            
        if hum > 85:
            st.warning(f"High Humidity Alert: {hum}% in {city}!")
            warning_shown = True
            
        if not warning_shown:
            st.success(f"All good in {city} (Temp: {temp}°C, Hum: {hum}%)")

st.markdown("---")

# ==========================================
# Data Analysis & Trends
# ==========================================
st.header(f"📈 Analytics & Deep Dive: {selected_city}")
city_df = df[df['City'] == selected_city].copy()

col1, col2, col3 = st.columns(3)
col1.metric("Average Temperature", f"{city_df['Temperature (C)'].mean():.2f} °C")
col2.metric("Max Temperature", f"{city_df['Temperature (C)'].max():.2f} °C")
col3.metric("Min Temperature", f"{city_df['Temperature (C)'].min():.2f} °C")

# Trend Chart
st.subheader("Temperature & Humidity Interactive Trend")
fig = px.line(city_df, x='Timestamp', y=['Temperature (C)', 'Humidity (%)'], 
              title=f"Detailed Historcal Trend ({selected_city})",
              markers=True,
              color_discrete_sequence=['#ff7f0e', '#1f77b4'])
fig.update_layout(hovermode="x unified", legend_title_text="Metric")
st.plotly_chart(fig, use_container_width=True)

# Comparisons
st.markdown("---")
st.subheader("🌐 Global City Comparison")
fig_comp = px.line(df, x='Timestamp', y='Temperature (C)', color='City', 
                   title="Temperature Comparison Across Tracked Cities",
                   markers=True)
fig_comp.update_layout(hovermode="x unified")
st.plotly_chart(fig_comp, use_container_width=True)

# ==========================================
# Machine Learning (Linear Regression)
# ==========================================
st.markdown("---")
st.header("🤖 Machine Learning Predictive Modeling")
st.markdown(f"Using **Linear Regression**, this module projects the potential temperature for **{selected_city}** over the next 12 hours based on recent historical trends.")

# Prepare Data
city_df['Epoch'] = city_df['Timestamp'].astype(int) // 10**9
X = city_df[['Epoch']]
y = city_df['Temperature (C)']

if len(X) > 5:  # Need adequate data to fit a reasonable line
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict future time steps (every 1 hour for 12 hours)
    last_datetime = city_df['Timestamp'].iloc[-1]
    future_datetimes = [last_datetime + timedelta(hours=i) for i in range(1, 13)]
    future_epochs = np.array([int(dt.timestamp()) for dt in future_datetimes]).reshape(-1, 1)
    
    predictions = model.predict(future_epochs)
    
    # Visualization for Prediction vs Historical
    fig_pred = go.Figure()
    
    # Historical Trace
    fig_pred.add_trace(go.Scatter(
        x=city_df['Timestamp'], 
        y=city_df['Temperature (C)'], 
        mode='lines+markers', 
        name='Historical Data',
        line=dict(color='#1f77b4')
    ))
    
    # Predictive Trace
    fig_pred.add_trace(go.Scatter(
        x=future_datetimes, 
        y=predictions, 
        mode='lines+markers', 
        name='Predicted (Next 12 Hours)',
        line=dict(dash='dash', color='#d62728', width=3)
    ))
    
    fig_pred.update_layout(
        title=f"Future Temperature Forecasting for {selected_city}",
        xaxis_title="Time", 
        yaxis_title="Temperature (°C)",
        hovermode="x unified"
    )
    st.plotly_chart(fig_pred, use_container_width=True)
    
    # Insight generator
    trend = "increasing" if predictions[-1] > predictions[0] else "decreasing"
    diff = abs(predictions[-1] - predictions[0])
    st.info(f"💡 **AI Insight**: Our model indicates a **{trend} trend**. Temperatures are projected to change by approximately **{diff:.2f}°C** over the next 12 hours.")
else:
    st.warning("Not enough historical data collected to train the prediction model robustly. Please allow the fetch script to gather more data points (minimum 6 required).")

# Footer
st.markdown("---")
st.markdown("Developed with Streamlit and scikit-learn. Data powered by OpenWeather API.")

