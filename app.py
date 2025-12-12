import streamlit as st
import requests
import datetime

# Function to fetch current weather da
def get_current_weather(city, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    return response.json()

# Function to fetch 5-day weather forecast data
def get_forecast(city, api_key):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    return response.json()

# Streamlit app
def main():
    st.set_page_config(page_title="Weather Forecast App", page_icon="⛅", layout="wide")

    # Sidebar menu
    with st.sidebar:
        selected = st.radio(
            "Main Menu",
            ["Home", "Current Weather", "5-Day Forecast"],
            index=1,
            format_func=lambda x: x.replace("_", " ")
        )

    st.title("Weather Forecast App")
    api_key = st.secrets["OWM_API_KEY"]["key"]
    city = st.text_input("Enter city name:")

    if city:
        if selected == "Current Weather":
            current_weather = get_current_weather(city, api_key)
            if current_weather.get("cod") != "404":
                st.subheader(f"Current Weather in {city}")
                st.metric("Temperature", f"{current_weather['main']['temp']}°C")
                st.write(f"**Weather:** {current_weather['weather'][0]['description'].capitalize()}")
                st.write(f"**Humidity:** {current_weather['main']['humidity']}%")
                st.write(f"**Wind Speed:** {current_weather['wind']['speed']} m/s")
            else:
                st.error("City not found. Please enter a valid city name.")
        elif selected == "5-Day Forecast":
            forecast = get_forecast(city, api_key)
            if forecast.get("cod") != "404":
                st.subheader("5-Day Forecast")
                for i in range(0, 40, 8):
                    day = forecast['list'][i]
                    date = datetime.datetime.fromtimestamp(day['dt']).strftime('%Y-%m-%d')
                    temp = day['main']['temp']
                    description = day['weather'][0]['description'].capitalize()
                    st.write(f"**Date:** {date}")
                    st.metric("Temperature", f"{temp}°C")
                    st.write(f"**Weather:** {description}")
                    st.write("---")
            else:
                st.error("City not found. Please enter a valid city name.")
if __name__ == "__main__":
    main()


