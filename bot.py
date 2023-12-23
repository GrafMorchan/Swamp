from aiogram import Bot, Dispatcher, executor, types
import requests
import json



bot = Bot('6736427112:AAEHhfnrqiPFLg6D4oFNpXMRVDpvotv6OW8')
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def info(message:types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Получить прогноз погоды в одном из городов', callback_data='city'))
    markup.add(types.InlineKeyboardButton('Список команд', callback_data='list'))
    await message.reply('Привет, тут вы можете узнать прогноз погоды через команды (/listCity и /start) соответсвтенно: ', reply_markup=markup)

@dp.message_handler(commands=['listCity'])
async def reply(message: types.Message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.InlineKeyboardButton('Perm'))
    markup.add(types.InlineKeyboardButton('Omsk'))
    markup.add(types.InlineKeyboardButton('Moscow'))
    await message.reply('Выводим данные! ', reply_markup=markup)

@dp.callback_query_handler()
async def callback(call):
    if call.data == 'list':
        await call.message.reply('/listCity\n/start')
    elif call.data == 'city':
        await call.message.reply('Введите название города: ')

@dp.message_handler(content_types=['text'])
async def reply(message:types.Message):
    city = message.text.lower().strip()
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&appid=34228359ab171356d14298a4ab559407&units=metric'
    res = requests.get(url)
    data = json.loads(res.text)
    if res.status_code==200:
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']
        desc = data['weather'][0]['description']

        comfortable = 37 - (37-temp)/(0.68-0.0014*humidity + 0.1*(1.76 + 1.4*wind_speed**0.75)) - 0.29*temp*(1-humidity/100)
        if (-50 <= comfortable) and (comfortable < -40):
            recomendat = "При столь низких температурах я вообще не рекомендовал бы вам выходить на улицу, но если нужда все ж затавила, то лучше принарядиться соответствующе: шапка с флисом (и/или балаклава), термобелье, толстая кофта, пуховик, варежки, пуховые штаны, вязанные носки и охотничие или военные берцы"
        elif (-40 < comfortable) and (comfortable <= -30):
            recomendat = "В такую холодрыгу стоит надеть: шапка с флисом (и/или балаклава), термобелье, пуховик, варежки, пуховые штаны, и охотничие или военные берцы"
        elif (-30 < comfortable) and (comfortable <= -20):
            recomendat = "Советуем: шапка с флисом (и/или балаклава), термобелье, куртка, перчатки, кожанные ботинки или зимние кроссовки"
        elif (-20 < comfortable) and (comfortable <= -10):
            recomendat = "Советуем: шапка, термобелье, ветровка, кожанные ботинки или зимние кроссовки"
        elif (-10 < comfortable) and (comfortable <= 0):
            recomendat = "Советуем: шапка, ветровка, кожанные ботинки или зимние кроссовки"
        elif (0 < comfortable) and (comfortable <= 10):
            recomendat = "Советуем: шапка, ветровка (или толстовка), кроссовки"
        elif (10 < comfortable) and (comfortable <= 20):
            recomendat = "Более, чем комфортная температура. Можно обойтись cпортивной одеждой"
        elif (20 < comfortable) and (comfortable <= 30):
            recomendat = "Жарковато, поэтому не забывайте о головном уборе"
        elif (30 < comfortable) and (comfortable <= 40):
            recomendat = "Избегайте прямых солнечных лучей и пейте больше воды. Рекомендуем укрыть лица"
        else:
            recomendat = "Экстримальная температура! Не покидайте дома!"
            
        await message.reply(f'Погода в городе: {message.text}\n'
                            f'Температура: {temp}*C\n (Ощущается как: {comfortable}*C)\n'
                            f'Влажность: {humidity}%\n'
                            f'Давление: {pressure}Ра\n'
                            f'Скорость ветра: {wind_speed} м/c\n'
                            f'Описание: {desc}\n'
                            f'{recomendat}')
    elif res.status_code == 404:
        await message.reply(f'Неизвестный город')

executor.start_polling(dp)
