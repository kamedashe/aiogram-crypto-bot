from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Импортируем функции (они те же по названию, но внутри теперь SQLAlchemy)
from database import get_all_items, get_item

router = Router()

@router.message(Command("shop"))
async def cmd_shop(message: types.Message):
    items = await get_all_items()
    
    if not items:
        await message.answer("Товаров нет 🤷‍♂️")
        return

    builder = InlineKeyboardBuilder()
    for item in items:
        # ВНИМАНИЕ: Обращаемся через точку (item.name), так как это Объект
        button_text = f"{item.name} — {item.price} $" 
        builder.button(text=button_text, callback_data=f"buy_{item.id}")
    
    builder.adjust(1)
    await message.answer("Выберите товар:", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("buy_"))
async def callback_buy(callback: types.CallbackQuery):
    item_id = int(callback.data.split("_")[1])
    item = await get_item(item_id)
    
    if item:
        # ТУТ ТОЖЕ ЧЕРЕЗ ТОЧКУ
        await callback.message.edit_text(
            f"✅ Вы выбрали: {item.name}.\n💰 К оплате: {item.price} $\n\nОформляем?"
        )
    else:
        await callback.message.edit_text("Товар не найден.")
    await callback.answer()