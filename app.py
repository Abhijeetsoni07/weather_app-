import streamlit as st
import requests
import json
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder
import os

# Page configuration
st.set_page_config(
    page_title="Weather App",
    page_icon="🌤️",
    layout="centered"
)

# API Configuration
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "adca00f74648052d5291270c8d23e9e1")
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

# Default timezone (India)
DEFAULT_TIMEZONE = "Asia/Kolkata"

def get_weather_data(city_name, api_key):
    """Fetch weather data from OpenWeatherMap API"""
    try:
        params = {
            "q": city_name,
            "appid": api_key,
            "units": "metric"
        }
        response = requests.get(WEATHER_API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {str(e)}")
        return None

def get_timezone_from_coords(lat, lon):
    """Get timezone from coordinates using TimezoneFinder"""
    try:
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=lat, lng=lon)
        return timezone_str if timezone_str else DEFAULT_TIMEZONE
    except Exception as e:
        st.warning(f"Could not determine timezone from coordinates: {str(e)}")
        return DEFAULT_TIMEZONE

def get_all_timezones():
    """Get list of all available timezones"""
    return pytz.all_timezones

def format_timezone_display(tz_name):
    """Format timezone name for better display"""
    return tz_name.replace("_", " ")

def get_current_time_in_timezone(tz_name):
    """Get current time in specified timezone"""
    try:
        tz = pytz.timezone(tz_name)
        return datetime.now(tz)
    except Exception as e:
        st.warning(f"Error getting time for timezone {tz_name}: {str(e)}")
        return None

# Main App
st.title("🌤️ Weather App")
st.markdown("Get weather information for any city and explore timezones!")

# Sidebar for API key input
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input(
        "OpenWeatherMap API Key",
        value=WEATHER_API_KEY,
        type="password",
        help="Get your free API key from https://openweathermap.org/api"
    )
    
    if api_key == "your_api_key_here" or not api_key:
        st.warning("⚠️ Please enter your OpenWeatherMap API key to use this app.")
        st.info("Get a free API key at: https://openweathermap.org/api")
    
    st.markdown("---")
    st.markdown("### 📝 Instructions")
    st.markdown("""
    1. Enter your OpenWeatherMap API key
    2. Enter a city name
    3. View weather information
    4. Explore timezones
    """)

# City input
city_name = st.text_input(
    "Enter City Name",
    placeholder="e.g., Mumbai, London, New York",
    help="Enter the name of the city you want weather information for"
)

if st.button("Get Weather", type="primary") or city_name:
    if not api_key or api_key == "your_api_key_here":
        st.error("❌ Please enter a valid API key in the sidebar first!")
    elif city_name:
        with st.spinner(f"Fetching weather data for {city_name}..."):
            weather_data = get_weather_data(city_name, api_key)
            
            if weather_data:
                # Extract weather information
                city = weather_data.get("name", city_name)
                country = weather_data.get("sys", {}).get("country", "")
                temp = weather_data.get("main", {}).get("temp", 0)
                feels_like = weather_data.get("main", {}).get("feels_like", 0)
                humidity = weather_data.get("main", {}).get("humidity", 0)
                pressure = weather_data.get("main", {}).get("pressure", 0)
                description = weather_data.get("weather", [{}])[0].get("description", "").title()
                wind_speed = weather_data.get("wind", {}).get("speed", 0)
                visibility = weather_data.get("visibility", 0)
                lat = weather_data.get("coord", {}).get("lat", 0)
                lon = weather_data.get("coord", {}).get("lon", 0)
                
                # Get timezone from coordinates
                city_timezone = get_timezone_from_coords(lat, lon)
                current_time = get_current_time_in_timezone(city_timezone)
                
                # Display weather information
                st.success(f"✅ Weather data retrieved for {city}, {country}")
                
                # Main weather display
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Temperature", f"{temp}°C")
                    st.metric("Feels Like", f"{feels_like}°C")
                    st.metric("Humidity", f"{humidity}%")
                
                with col2:
                    st.metric("Pressure", f"{pressure} hPa")
                    st.metric("Wind Speed", f"{wind_speed} m/s")
                    st.metric("Visibility", f"{visibility/1000:.1f} km" if visibility else "N/A")
                
                st.markdown("---")
                
                # Weather description
                st.subheader(f"🌦️ {description}")
                
                # Timezone information
                st.markdown("### 🕐 Timezone Information")
                if current_time:
                    st.info(f"**City Timezone:** {format_timezone_display(city_timezone)}")
                    st.info(f"**Current Time:** {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
                
                # Timezone selector
                st.markdown("### 🌍 Explore All Timezones")
                st.markdown("Select a timezone to see the current time:")
                
                # Filter timezones
                timezone_filter = st.text_input(
                    "Filter timezones (optional)",
                    placeholder="e.g., Asia, America, Europe",
                    help="Type to filter timezones by region"
                )
                
                all_timezones = get_all_timezones()
                if timezone_filter:
                    filtered_timezones = [tz for tz in all_timezones if timezone_filter.lower() in tz.lower()]
                else:
                    filtered_timezones = all_timezones
                
                # Default to India timezone
                default_index = 0
                if DEFAULT_TIMEZONE in filtered_timezones:
                    default_index = filtered_timezones.index(DEFAULT_TIMEZONE)
                
                selected_timezone = st.selectbox(
                    "Select Timezone",
                    filtered_timezones,
                    index=default_index,
                    format_func=format_timezone_display
                )
                
                # Display time in selected timezone
                selected_time = get_current_time_in_timezone(selected_timezone)
                if selected_time:
                    st.success(f"**Current time in {format_timezone_display(selected_timezone)}:** {selected_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
                
                # Additional information
                with st.expander("📍 Location Details"):
                    st.write(f"**Latitude:** {lat}°")
                    st.write(f"**Longitude:** {lon}°")
                    st.write(f"**Country Code:** {country}")
                
                with st.expander("📊 Raw Weather Data"):
                    st.json(weather_data)
            else:
                st.error("❌ Could not fetch weather data. Please check the city name and API key.")
    else:
        st.warning("⚠️ Please enter a city name")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Powered by OpenWeatherMap API | Made with Streamlit"
    "</div>",
    unsafe_allow_html=True
)

