import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import aiohttp
from dotenv import load_dotenv

# Загружаем переменные из .env (для локальной разработки)
load_dotenv()

# Получаем токен из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Не найден токен бота! Установите переменную окружения BOT_TOKEN")

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(
        "🐱 Привет! Я бот с котиками.\n"
        "Отправь команду /cat чтобы получить случайного котика!"
    )

@dp.message(Command("cat"))
async def send_random_cat(message: types.Message):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://cataas.com/cat') as response:
                if response.status == 200:
                    await message.answer_photo(photo='https://cataas.com/cat')
                else:
                    await message.answer("😿 Не удалось загрузить котика.")
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
