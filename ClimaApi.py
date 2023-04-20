import requests
import json

# API key para OpenWeatherMap
clima_apikey = "8a8d019579f82cdbeb731c411f8e7260"

# API key para Google Maps
maps_apikey = "AIzaSyCkBQRemsS63pP0jKTV_55A4wRarHP3Qak"

# URL base para OpenWeatherMap
url_clima = "https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid={api_key}"

# URL base para Google Maps
url_maps = "https://maps.googleapis.com/maps/api/geocode/json?key={api_key}&address={address}&components=country"

def clima(city):
    url = url_clima.format(city=city, api_key=clima_apikey)
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = json.loads(response.text)
        return weather_data
    else:
        return None

def lugar(city):
    url = url_maps.format(api_key=maps_apikey, address=city)
    response = requests.get(url)
    if response.status_code == 200:
        location_data = json.loads(response.text)
        if location_data["status"] == "OK":
            components = location_data["results"][0]["address_components"]
            country = None
            for c in components:
                if "country" in c["types"]:
                    country = c["long_name"]
                    break
            return {"lat": location_data["results"][0]["geometry"]["location"]["lat"],
                    "lng": location_data["results"][0]["geometry"]["location"]["lng"],
                    "country": country}
        else:
            return None
    else:
        return None

def lugar_del_clima(city):
    location = lugar(city)
    if location is not None:
        weather = clima(city)
        if weather is not None:
            temp_f = weather['main']['temp']
            temp_c = round((temp_f - 32) / 1.8, 1)
            return {"city": city, "latitude": location["lat"], "longitude": location["lng"], "country": location["country"], "weather": weather, "temp_c": temp_c}
    return None

city = input("Ciudad: ")
weather_location = lugar_del_clima(city)
if weather_location is not None:
    print(f"País: {weather_location['country']}")
    print(f"Latitud: {weather_location['latitude']}")
    print(f"Longitud: {weather_location['longitude']}")
    print(f"Clima: {weather_location['weather']['weather'][0]['main']}")
    print(f"Temperatura: {weather_location['temp_c']}°C")
else:
    print("No se pudo obtener la información del clima y la ubicación correspondiente.")
    