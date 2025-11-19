from aiogram import Router, types
from aiogram.filters import Command

router = Router()

# Хэндлер на команду /start (перенесем его сюда, это логичнее)
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! 👋\n\n"
        "Я умею:\n"
        "🛒 /shop — Купить товары\n"
        "📈 /btc — Курс Биткоина"
    )

# Хэндлер на ЛЮБОЕ текстовое сообщение (Catch-all)
# Важно: он должен быть зарегистрирован ПОСЛЕДНИМ в main.py
@router.message() 
async def echo_handler(message: types.Message):
    # Мы не просто эхом отвечаем, а подсказываем
    await message.answer(
        "Я не понимаю этот текст 🤖\n\n"
        "Используй команды:\n"
        "🛒 /shop — Магазин\n"
        "📈 /btc — Крипта"
    )