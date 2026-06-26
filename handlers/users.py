from aiogram import Router, F, types
from aiogram.filters import CommandStart

from database import add_user, get_user
from keyboards import get_main_keyboard

users_router = Router()

@users_router.message(CommandStart())
async def cmd_start(message: types.Message):
    add_user(tg_id=message.from_user.id, name=message.from_user.first_name)
    await message.answer(
        f"🎂 Привет, {message.from_user.first_name}!\n"
        "Ты успешно занесен в базу данных кондитерской!",
        reply_markup=get_main_keyboard()
    )


@users_router.message(F.text == "cabinet")
async def show_cabinet(message: types.Message):
    user_name = get_user(message.from_user.id)
    if user_name:
        await message.answer(f"👤 Личный кабинет\n\nРады видеть тебя, {user_name}!")
    else:
        await message.answer("Профиль не найден. Пожалуйста, введите команду /start для регистрации.")