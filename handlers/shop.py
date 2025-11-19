from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Импорт из папки выше (..) может быть сложным для новичка,
# поэтому пока просто импортируем из database, считая что запускаем из корня.
from database import get_all_items, get_item

# Создаем Роутер (отдел магазина)
router = Router()

# Заменили @dp.message на @router.message
@router.message(Command("shop"))
async def cmd_shop(message: types.Message):
    items = await get_all_items()
    if not items:
        await message.answer("Товаров нет 🤷‍♂️")
        return

    builder = InlineKeyboardBuilder()
    for item in items:
        button_text = f"{item['name']} — {item['price']} руб"
        builder.button(text=button_text, callback_data=f"buy_{item['id']}")
    
    builder.adjust(1)
    await message.answer("Выберите товар:", reply_markup=builder.as_markup())

# Заменили @dp.callback_query на @router.callback_query
@router.callback_query(F.data.startswith("buy_"))
async def callback_buy(callback: types.CallbackQuery):
    item_id = callback.data.split("_")[1]
    item = await get_item(item_id)
    
    if item:
        await callback.message.edit_text(
            f"✅ Вы выбрали: {item['name']}.\n💰 К оплате: {item['price']} руб.\n\nОформляем?"
        )
    else:
        await callback.message.edit_text("Товар не найден.")
    await callback.answer()