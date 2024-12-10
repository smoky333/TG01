from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import asyncio
import requests
from config import TOKEN  # Убедитесь, что в config.py указан ваш токен

# API-ключ для OpenWeatherMap
WEATHER_API_KEY = '396c2829c4d848d0da39cd947999a7fa'

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для получения погоды
def get_weather(city):
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru'
        response = requests.get(url)
        response.raise_for_status()  # Проверяем, что запрос успешен
        data = response.json()
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        return f'Погода в {city.capitalize()}:\nТемпература: {temp}°C\nОписание: {description.capitalize()}'
    except requests.exceptions.HTTPError:
        return 'Не удалось получить данные о погоде. Проверьте название города.'
    except Exception as e:
        return f'Произошла ошибка: {e}'


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот для прогноза погоды.\n"
        "Введите /weather <город>, чтобы узнать погоду в нужном городе.\n"
        "Пример: /weather Москва"
    )


@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Доступные команды:\n"
        "/start - Начать работу\n"
        "/help - Помощь\n"
        "/weather <город> - Узнать погоду в указанном городе\n\n"
        "Пример: /weather Москва"
    )

# Обработка команды /weather
@dp.message(Command("weather"))
async def cmd_weather(message: Message):
    # Получение города из сообщения
    command_parts = message.text.split(maxsplit=1)
    if len(command_parts) < 2:
        await message.answer("Пожалуйста, укажите город после команды. Пример: /weather Москва")
        return

    city = command_parts[1].strip()  # Получаем название города
    weather_info = get_weather(city)
    await message.answer(weather_info)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
