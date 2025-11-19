from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.crypto_api import get_btc_price

router = Router()

def get_refresh_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔄 Обновить", callback_data="refresh_btc")
    return builder.as_markup() # Исправил buildeer на builder

@router.message(Command("btc"))
async def cmd_btc(message: types.Message):
    price = await get_btc_price()

    print(f"👀 [HANDLER DEBUG] Хэндлер получил цену: {price}")

    # ИСПРАВЛЕННАЯ ЛОГИКА 👇
    if price is None: 
        await message.answer("Не удалось получить данные 😔")
        return
    
    # Если мы здесь — значит цена есть!
    await message.answer(
        f"💰 Текущая цена BTC: {price} $",
        reply_markup=get_refresh_keyboard()
    )

@router.callback_query(F.data == "refresh_btc")
async def callback_refresh_btc(callback: types.CallbackQuery):
    price = await get_btc_price()

    # ИСПРАВЛЕННАЯ ЛОГИКА 👇
    if price is None:
        await callback.answer("Ошибка получения данных", show_alert=True)
        return
    
    try:
        await callback.message.edit_text(
            f"💰 Текущая цена BTC: {price} $",
            reply_markup=get_refresh_keyboard()
        )
    except Exception:
        pass 

    await callback.answer("Обновлено!")