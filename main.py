import asyncio
import logging
import os 

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

# Импортируем инициализацию БД
from database import init_db
# Импортируем наш роутер из папки handlers
from handlers.shop import router as shop_router
from handlers.crypto import router as crypto_router
from handlers.common import router as common_router

# 1. Загружаем переменные из файла .env
load_dotenv()

# 2. Достаем токен 
TOKEN = os.getenv("BOT_TOKEN")

async def main():
    # 1. Запускаем БД
    await init_db()

    # Небольшая проверка, чтобы не тупить, если забыл создать .env
    if not TOKEN:
        print("Ошибка: Токен не найден! Проверь файл .env")
        return
    
    # 2. Настройка бота
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    # 3. ВАЖНО: Подключаем роутеры к диспетчеру
    dp.include_router(shop_router)
    dp.include_router(crypto_router)
    dp.include_router(common_router)
    
    
    print("Бот запущен (безопасно)! 🔒")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")