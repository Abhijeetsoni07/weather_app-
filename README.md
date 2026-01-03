# Weather App with Timezone Explorer

A beautiful Streamlit application that fetches weather information for any city and allows you to explore all available timezones.

## Features

- 🌤️ **Weather Information**: Get real-time weather data for any city
- 🕐 **Timezone Detection**: Automatically detects the timezone of the searched city
- 🌍 **Timezone Explorer**: Browse and view current time in any timezone worldwide
- 🔍 **Timezone Filtering**: Filter timezones by region (Asia, America, Europe, etc.)
- 📊 **Detailed Weather Data**: Temperature, humidity, pressure, wind speed, visibility, and more

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get API Key

1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Get your API key from the dashboard
4. The free tier includes 60 calls per minute

### 3. Run the App

**Option 1: Using Streamlit command**
```bash
streamlit run app.py
```

**Option 2: Set API key as environment variable (optional)**
```bash
# Windows PowerShell
$env:WEATHER_API_KEY="your_api_key_here"
streamlit run app.py

# Linux/Mac
export WEATHER_API_KEY="your_api_key_here"
streamlit run app.py
```

### 4. Use the App

1. Enter your OpenWeatherMap API key in the sidebar
2. Enter a city name in the main input field
3. Click "Get Weather" or press Enter
4. View weather information and explore timezones!

## Default Timezone

The app defaults to **India (Asia/Kolkata)** timezone as requested.

## API Information

This app uses the **OpenWeatherMap API** (free tier):
- Current Weather Data endpoint
- No credit card required for free tier
- 60 API calls per minute limit

## Requirements

- Python 3.7+
- Streamlit
- requests
- pytz
- timezonefinder

## License

This project is open source and available for personal and commercial use.

