from weather import WeatherData
import telebot
from dotenv import dotenv_values
from pathlib import Path

from telebot import types
from test_volga import parsePage

_ENV_ARG = dotenv_values(Path(".env"))

bot = telebot.TeleBot(_ENV_ARG["TG_TOKEN"])

coordinates = {
    "south": ['53.16247', '50.18027'],
    "dirty": ['53.23666', '50.12478'],
    "danube": ['53.22981', '50.1542']
}


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, сейчас я расскажу тебе погоду на сегодня.")
        keyboard = types.InlineKeyboardMarkup()

        key_south = types.InlineKeyboardButton(text='Южный мост', callback_data='south')
        keyboard.add(key_south)
        key_dirty = types.InlineKeyboardButton(text='Грязный', callback_data='dirty')
        keyboard.add(key_dirty)
        key_danube = types.InlineKeyboardButton(text='Дунай', callback_data='danube')
        keyboard.add(key_danube)
        key_water_level = types.InlineKeyboardButton(text='Уровень и температура воды', callback_data='water_lvl')
        keyboard.add(key_water_level)

        bot.send_message(message.from_user.id, text='Выбери место', reply_markup=keyboard)

    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши Привет")

    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    weather_list = ["danube", "south", "dirty"]
    if call.data in weather_list:
        try:
            data = WeatherData(coordinates[call.data])
            object_weather = data.get_weather_data_now()

            weather_status = data.search_weather_by_id(object_weather)
            temp = data.get_temp(object_weather)
            pressure = data.get_pressure(object_weather)
            visibility = data.get_visibility(object_weather)
            humidity = data.get_humidity(object_weather)
            speed_wind = data.get_speed_wind(object_weather)
            sunrise_and_sunset_times = data.get_sunrise_and_sunset_times(object_weather)
            rain_3h = data.get_rain_3h(object_weather)
            snow_3h = data.get_snow_3h(object_weather)

            msg = f'{weather_status}\nТемпература воздуха {temp[0]}°C, ощущается как {temp[1]}°C\nДавление {pressure}\n' \
                  f'Видимость {visibility} метров\nВлажность {humidity}%\n' \
                  f'Скорость ветра {speed_wind[0]} м\с. Порывы до {speed_wind[1]} м\с. Направление {speed_wind[2]}\n' \
                  f'Закат солнца {sunrise_and_sunset_times[0]}\nВосход солнца {sunrise_and_sunset_times[1]}\n' \
                  f'Кол-во осадков дождя за 3 часа {rain_3h}\n' \
                  f'Кол-во осадков снега за 3 часа {snow_3h} '
        except:
            msg = 'При запросе произошла ошибка'

    elif call.data == "water_lvl":
        msg = 'Дата            Уровень воды\n'

        water_lvl_list = parsePage()
        for i in water_lvl_list:
            for j in i:
                if "-" in j:
                    msg += f"{str(j)}            "
                else:
                    msg += f"{str(j)}\n"

    bot.send_message(call.message.chat.id, msg)


bot.polling(none_stop=True, interval=0, timeout=123)
