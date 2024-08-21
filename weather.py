import json
import requests
import time

from dotenv import dotenv_values
from pathlib import Path

_ENV_ARG = dotenv_values(Path(".env"))

class WeatherData(object):
    api_key = _ENV_ARG["API_KEY"]

    def __init__(self, lat_lot: list):
        self.lat = lat_lot[0]
        self.lot = lat_lot[1]

    def get_weather_data_now(self):
        try:
            response_data_weather = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?units=metric&lang=ru&lat="
                f"{self.lat}&lon={self.lot}&&APPID={self.api_key}").json()
            with open('response_weather.json', 'w', encoding='utf-8') as f:
                f.write(str(response_data_weather))

            return response_data_weather

        except:
            return None

    def search_weather_by_id(self, data: object):
        id_weather = str(data["weather"][0]["id"])
        with open('1.json', 'r', encoding='utf-8') as f:
            id_list = json.load(f)

        return id_list[id_weather]

    def get_temp(self, data: object):
        temp = data["main"]["temp"]
        feels_like_temp = data["main"]["feels_like"]

        return [temp, feels_like_temp]

    def get_pressure(self, data: object):
        pressure = int(data["main"]["pressure"])

        return str(pressure / 1.333)

    def get_visibility(self, data: object):
        visibility = data["visibility"]

        return visibility

    def get_humidity(self, data: object):
        humidity = data["main"]["humidity"]

        return humidity

    def get_speed_wind(self, data: object):
        speed_wind = data["wind"]["speed"]
        gust_wind = data["wind"]["gust"]
        deg_wind_degrees = data["wind"]["deg"]
        wind_list = [speed_wind, gust_wind]

        if 0 <= deg_wind_degrees <= 22.5 or 337.5 <= deg_wind_degrees < 360:
            direction_wind = "C"
            wind_list.append(direction_wind)

        elif 22.5 < deg_wind_degrees < 67.5:
            direction_wind = "СВ"
            wind_list.append(direction_wind)

        elif 67.5 <= deg_wind_degrees <= 112.5:
            direction_wind = "В"
            wind_list.append(direction_wind)

        elif 112.5 < deg_wind_degrees < 157.5:
            direction_wind = "ЮВ"
            wind_list.append(direction_wind)

        elif 157.5 <= deg_wind_degrees <= 202.5:
            direction_wind = "Ю"
            wind_list.append(direction_wind)

        elif 202.5 < deg_wind_degrees < 247.5:
            direction_wind = "ЮЗ"
            wind_list.append(direction_wind)

        elif 247.5 <= deg_wind_degrees <= 292.5:
            direction_wind = "З"
            wind_list.append(direction_wind)

        elif 292.5 < deg_wind_degrees < 337.5:
            direction_wind = "СЗ"
            wind_list.append(direction_wind)

        else:
            direction_wind = "Направление не определенно"
            wind_list.append(direction_wind)

        return wind_list

    def get_sunrise_and_sunset_times(self, data: object):
        sunset = self.сonverting_unix_times_to_understandable_dates(data["sys"]["sunset"])
        sunrise = self.сonverting_unix_times_to_understandable_dates(data["sys"]["sunrise"])

        return [sunset, sunrise]

    def сonverting_unix_times_to_understandable_dates(self, unix_date):
        human_date = time.strftime(" %d %b %Y %H:%M ", time.localtime(unix_date))

        return human_date

    def get_rain_3h(self, data: object):
        try:
            rain_last_3h = data["rain"]["3h"]
            return f"{rain_last_3h} мм"
        except:
            return "дождя нет"

    def get_snow_3h(self, data: object):
        try:
            snow_last_3h = data["snow"]["3h"]
            return f"{snow_last_3h} мм"
        except:
            return "снега нет"
