from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardMarkup

from database import get_all_cakes

def get_main_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.add(types.KeyboardButton(text="MENU"))
    builder.add(types.KeyboardButton(text="deliver"))
    builder.add(types.KeyboardButton(text="cabinet"))

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)



def get_menu_keyboard():
    builder = InlineKeyboardBuilder()
   
    cakes = get_all_cakes()

    for code, name, price in cakes:
        builder.add(types.InlineKeyboardButton(
            text=f"{name} - {price}som",
            callback_data=f"buy_{code}"
        ))

    builder.adjust(1)
    return builder.as_markup()



def get_address_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Всё верно", callback_data="confirm_address")
    builder.button(text="✏️ Изменить адрес", callback_data="change_address")
    builder.adjust(2)
    return builder.as_markup() 