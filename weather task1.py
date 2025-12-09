import requests
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(
    page_title="Real-Time Weather Information System",
    layout="centered"
)

st.title("Real-Time Weather Information System")
st.subheader("Internship Project Using Public Weather API")
st.write(
    "This application allows users to select a city and view real-time weather "
    "information along with graphical visualization."
)

st.divider()

st.header("City Selection")
city = st.text_input("Enter City Name:")
get_weather = st.button("Get Weather Report")

if get_weather and city:
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()

    if "results" not in geo_data:
        st.error("City not found. Please check the spelling and try again.")
    else:
        latitude = geo_data["results"][0]["latitude"]
        longitude = geo_data["results"][0]["longitude"]
        country = geo_data["results"][0]["country"]

        st.success(f"Location Detected Successfully: {city}, {country}")
        st.write(f"Latitude: {latitude}")
        st.write(f"Longitude: {longitude}")

        st.divider()

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}&longitude={longitude}"
            f"&hourly=temperature_2m&current_weather=true"
        )

        weather_response = requests.get(weather_url)
        data = weather_response.json()

        current_temp = data["current_weather"]["temperature"]
        current_wind = data["current_weather"]["windspeed"]

        st.header("Current Weather Report")
        st.write(f"Temperature: {current_temp} °C")
        st.write(f"Wind Speed: {current_wind} km/h")

        st.divider()

        st.header("Hourly Temperature Data")
        time_data = data["hourly"]["time"][:10]
        temp_data = data["hourly"]["temperature_2m"][:10]

        df = pd.DataFrame({
            "Time": time_data,
            "Temperature (°C)": temp_data
        })

        st.dataframe(df, use_container_width=True)

        st.divider()

        st.header("Temperature Visualization")
        fig, ax = plt.subplots()
        ax.plot(df["Time"], df["Temperature (°C)"], marker="o")
        ax.set_xlabel("Time")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title(f"Hourly Temperature Forecast - {city}")
        plt.xticks(rotation=45)

        st.pyplot(fig)

        st.divider()

        st.caption("Weather data provided by Open-Meteo Public API | Internship Project")

elif get_weather and not city:
    st.warning("Please enter a city name before clicking the button.")
