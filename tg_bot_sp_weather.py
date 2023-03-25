import requests
import os
import logging
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)


def get_eclipse_data():
    url = 'https://www.timeanddate.com/eclipse/list.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    eclipse_info = soup.find_all('a', {'class': 'ec-link'})
    result = []
    for i in range(2):
        eclipse_type = eclipse_info[i].find('span', {'class': 'ec-type'}).text
        eclipse_date = eclipse_info[i].find('span', {'class': 'ec-date'}).text
        eclipse_location = eclipse_info[i].find('span', {'class': 'ec-where'}).text
        result.append(f'{eclipse_type}, дата {eclipse_date}, место {eclipse_location}')
    return '\n'.join(result)


def get_sunspot_data():
    url = 'https://services.swpc.noaa.gov/json/goes/primary/xray-flares-latest.json'
    response = requests.get(url)
    data = response.json()
    sunspot_class = data[0]['max_class']
    sunspot_date = data[0]['time_tag']
    latest_sunspot = f'Последняя вспышка класса {sunspot_class} произошла {sunspot_date}'
    return latest_sunspot


def get_geo_activity():
    url = 'https://services.swpc.noaa.gov/json/planetary_k_index_1m.json'
    response = requests.get(url)
    data = response.json()
    kp_index = data[-1]['kp_index']
    kp_date = data[-1]['time_tag']
    latest_kp_index = f'KP индекс на дату {kp_date} составил {kp_index}'
    return latest_kp_index


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.reply('Привет! Я бот космической погоды. Используйте /help, чтобы узнать, что я могу делать.')


@dp.message_handler(commands=['help'])
async def help_handler(message: types.Message):
    help_text = 'Я могу предоставить следующую информацию:\n'
    help_text += '/eclipse - информация о ближайших солнечном и лунном затмениях\n'
    help_text += '/sunspot - информация о последних солнечных вспышках\n'
    help_text += '/kp - информация о последнем KP индексе\n'
    await message.reply(help_text)


@dp.message_handler(commands=['eclipse'])
async def eclipse_handler(message: types.Message):
    eclipse_data = get_eclipse_data()
    await message.reply(eclipse_data)


@dp.message_handler(commands=['sunspot'])
async def sunspot_handler(message: types.Message):
    sunspot_data = get_sunspot_data()
    await message.reply(sunspot_data)


@dp.message_handler(commands=['kp'])
async def kp_handler(message: types.Message):
    kp_data = get_geo_activity()
    await message.reply(kp_data)


if __name__ == '__main__':
    executor.start_polling(dp)
