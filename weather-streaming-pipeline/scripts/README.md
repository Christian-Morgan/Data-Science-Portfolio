# 🌤 Weather Stream to Azure Event Hubs

This script continuously collects **real-time weather data** from the [OpenWeatherMap API](https://openweathermap.org/api) and streams it to **Azure Event Hubs** for downstream processing or analytics.

## How It Works
1. The script calls the OpenWeather API for a list of cities.  
2. It converts the response into JSON format.  
3. The data is sent as events to **Azure Event Hubs** using the Python SDK.  
4. The process repeats automatically every 5 minutes.

## Key Components
- **`api_call()`** — Fetches weather data for a given city.  
- **`api_call_timer()`** — Runs the API calls in a loop and sends results to Event Hubs.  
- **Azure EventHubProducerClient** — Handles batch creation and event publishing.  

## Running the Script
1. Add your credentials:
   ```python
   EVENT_HUB_CONN_STR = "<your-event-hub-connection-string>"
   EVENT_HUB_NAME = "<your-event-hub-name>"
   API_KEY = "<your-openweather-api-key>"
2. Run the `weather_producer.py` script.
3. Stop it anytime with **Ctrl + C.**
