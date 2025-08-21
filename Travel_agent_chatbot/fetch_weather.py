import requests

API_KEY = "xxxxxxxxxxxxxxxxxxxxx"

def main(location: str) -> str:
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": API_KEY,
        "units": "metric",
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if response.status_code == 200:
        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return {
            "result": f"{location}: {weather_desc}, Temperature: {temp}°C"
        }
    else:
        return {
            "result": "Could not retrieve weather data",
        }
