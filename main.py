import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # Используем MemoryStorage
from aiogram.utils.exceptions import Throttled  # Импортируем исключение Throttled
from datetime import datetime

API_TOKEN = '7340059630:AAHy-ZSI7rL46SzrOM0yGtbdivo0ltZq-Lg'

# Инициализация хранилища
storage = MemoryStorage()  # Используем хранилище в памяти

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)  # Передаем хранилище в диспетчер

# ID канала для пересылки сообщений
CHANNEL_ID = '-4229504298'  # Укажи ID твоего канала

# Приветственное сообщение
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я анонимный бот. Напиши что-нибудь, и я передам это анонимно.")

# Логирование сообщений для админов
async def log_message(message: types.Message):
    log_text = f"[{datetime.now()}] User ID {message.from_user.id} отправил сообщение: {message.text}"
    logging.info(log_text)  # Логирование в консоль

# Фильтрация контента и антиспам
@dp.message_handler(content_types=types.ContentType.ANY)
async def handle_message(message: types.Message):
    try:
        # Ограничение по количеству сообщений (антиспам)
        await dp.throttle('message', rate=2)  # Пример: 1 сообщение в минуту

        # Фильтрация по типам контента
        if message.content_type == 'text':
            await bot.send_message(CHANNEL_ID, message.text)
            await message.reply("Твое текстовое сообщение отправлено анонимно!")
        elif message.content_type == 'photo':
            await bot.send_photo(CHANNEL_ID, message.photo[-1].file_id, caption=message.caption)
            await message.reply("Твое фото отправлено анонимно!")
        elif message.content_type == 'video':
            await bot.send_video(CHANNEL_ID, message.video.file_id, caption=message.caption)
            await message.reply("Твое видео отправлено анонимно!")
        else:
            await message.reply("Поддерживаются только текст, фото и видео.")

        # Логирование отправленного сообщения
        await log_message(message)

    except Throttled as throttled:  # Ловим исключение Throttled
        await message.reply(f"Слишком много сообщений! Подожди {throttled.rate} секунд перед отправкой следующего.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
