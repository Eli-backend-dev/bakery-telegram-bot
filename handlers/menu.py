from aiogram import Router, F, types

from keyboards import get_menu_keyboard
from database import add_order, get_cake_name

menu_router = Router()

@menu_router.message(F.text == "MENU")
async def show_menu(message: types.Message):
    await message.answer(
        "🎂 **Наше Меню** 🎂\n\nВыбирай скорее, всё свежее и безумно вкусное:",
        reply_markup=get_menu_keyboard(),
        parse_mode="Markdown"
    )


@menu_router.callback_query(F.data.startswith("buy_"))
async def process_buy_dessert(callback: types.CallbackQuery):
    dessert_code = callback.data.split("_")[1]
    chosen_dessert = get_cake_name(dessert_code)

    user_id = callback.from_user.id

    add_order(user_id=user_id, cake_code=dessert_code)

    await callback.message.answer(f"✅ {chosen_dessert} добавлен в корзину!🛒")
    await callback.answer()