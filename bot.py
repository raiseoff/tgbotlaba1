from config import token
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

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!", reply_markup = kb)
@dp.message(Command("code"))
async def custom_command_code(message: Message) -> None:
    await message.answer(f"Github open source code: https://github.com/raiseoff/tgbotlaba1.git")

kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Фото'), KeyboardButton(text='Аудио')]
],
resize_keyboard=True)

@dp.message(F.text == "Фото")
async def send_photo(message: Message) -> None:
    photoBoo = FSInputFile('images/Boo.jpg')
    await message.answer_photo(photo=photoBoo)

@dp.message(F.text == "Аудио")
async def send_audio(message: Message) -> None:
    audioBoo = FSInputFile('audios/Boo2.mp3')
    await message.answer_audio(audio=audioBoo)

async def main() -> None:
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
asyncio.run(main())