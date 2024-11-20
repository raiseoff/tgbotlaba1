import os

import requests
from yt_dlp import YoutubeDL
import imageio_ffmpeg
from config import token, photoAPI
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, FSInputFile, CallbackQuery

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
        image_url = get_image_url(msg.text)
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
async def request_audio_query(message: Message):
    await message.answer("Напишите название или ссылку на YouTube-видео для загрузки аудио:")

    @dp.message(lambda msg: msg.from_user.id == message.from_user.id)
    async def handle_audio_query(msg: Message):
        query = msg.text
        audio_file = download_audio_from_youtube(query)
        if audio_file:
            # Используем FSInputFile для отправки локального файла
            audio = FSInputFile(audio_file)
            await msg.reply_audio(audio=audio)
            os.remove(audio_file)  # Удаляем файл после отправки
        else:
            await msg.reply("Извините, не удалось загрузить аудио. Попробуйте другой запрос.")

        dp.message.handlers.pop()  # Удаляем временный обработчик

def download_audio_from_youtube(query: str) -> str:
    """Загружает аудио из YouTube и возвращает путь к MP3-файлу."""
    try:
        # Папка для временных файлов
        output_dir = "downloads"
        os.makedirs(output_dir, exist_ok=True)
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        ydl_opts = {
            'format': 'bestaudio/best',  # Загружаем лучшее аудио
            'outtmpl': f'{output_dir}/%(title)s.%(ext)s',  # Путь и имя файла
            'extractaudio': True,  # Извлечение только аудио
            'audioquality': 1,  # Лучшее качество
            'postprocessors': [],  # Без постобработки
            'ffmpeg_location': ffmpeg_path,  # Указываем путь к ffmpeg
            'default_search': 'ytsearch',  # Поиск по запросу
        }

        with YoutubeDL(ydl_opts) as ydl:
            # Получаем информацию о видео (или плейлисте)
            info = ydl.extract_info(query, download=True)
            # Если это плейлист, возьмем первый элемент из 'entries'
            if 'entries' in info:
                video_info = info['entries'][0]  # Первый файл из плейлиста
            else:
                video_info = info  # Просто видео, без плейлиста
            # Получаем название из fulltitle или title
            file_name = video_info.get('fulltitle', video_info.get('title', 'downloaded_audio'))
            file_path = os.path.join(output_dir, f"{file_name}.webm")
            # Переименовываем файл в mp3
            new_file_path = file_path.replace('.webm', '.mp3')
            os.rename(file_path, new_file_path)
            return new_file_path
    except Exception as e:
        logging.error(f"Ошибка при загрузке аудио: {e}")
        return None
























@dp.message(Command("stop"))
async def stop_command_handler(message: Message) -> None:
    await message.answer("Бот остановлен")
    await dp.stop_polling()



async def main() -> None:
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
asyncio.run(main())