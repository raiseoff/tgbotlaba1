import requests

from config import token, photoAPI
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, FSInputFile

dp = Dispatcher()
#Dispatcher отвечает за маршрутизацию сообщений и событий, получаемых ботом, к соответствующим обработчикам. Этот объект нужен для добавления обработчиков команд, сообщений и других событий.

kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Фото'), KeyboardButton(text='Аудио')]
],
resize_keyboard=True,
one_time_keyboard=False,
remove_keyboard=True)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!", reply_markup = kb)
@dp.message(Command("code"))
async def custom_command_code(message: Message) -> None:
    await message.answer(f"Github open source code: https://github.com/raiseoff/tgbotlaba1.git", reply_markup = kb)

@dp.message(F.text == "Фото")
async def send_photo(message: Message):
    await message.answer(f"Напишите ваш запрос")
    @dp.message(lambda msg: msg.from_user.id == message.from_user.id)
    async def handle_query(msg: Message):
        query = msg.text
        image_url = get_image_url(query)
        if image_url:
            await msg.reply_photo(photo=image_url, reply_markup = kb)
        else:
            await msg.reply("Извините, не удалось найти изображение по вашему запросу.", reply_markup = kb)

        # Удаляем обработчик после выполнения, чтобы не обрабатывать другие сообщения
        dp.message.handlers.pop()

def get_image_url(query: str) -> str:
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={photoAPI}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data["urls"]["regular"]  # Возвращает URL для изображения среднего размера
    else:
        return None

@dp.message(F.text == "Аудио")
async def send_audio(message: Message) -> None:
    audio_url = 'https://uzmuza.com/files/mp3/mp3-2024/kot-mem-bu-ispugalsya-ne-boysya-ya-drug.mp3'
    await message.answer_audio(audio=audio_url)

@dp.message(Command("stop"))
async def stop_command_handler(message: Message) -> None:
    await message.answer("Бот остановлен")
    await dp.stop_polling()



async def main() -> None:
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
asyncio.run(main())