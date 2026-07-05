from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext 
from aiogram.types import Message
from aiogram import F, Router, types

from keyboards import get_address_keyboard
from database import update_user_address , get_user_address



deliver_router = Router()

class DeliveryStates(StatesGroup):
    waiting_for_address = State()




@deliver_router.message(F.text == "deliver") 
async def start_delivery(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    current_address=get_user_address(tg_id)

    if current_address:
        await message.answer(
            f"Я помню ваш адрес:\n📍 {current_address}\n\nВсё верно или хотите изменить?",
            reply_markup=get_address_keyboard(),
            parse_mode="HTML"
        )
    else:
        # Если адреса нет в базе — включаем FSM и спрашиваем с нуля, как раньше
        await message.answer("Введите ваш адрес доставки:")
        await state.set_state(DeliveryStates.waiting_for_address) 



@deliver_router.message(DeliveryStates.waiting_for_address) 
async def process_deliver(message: Message, state: FSMContext):
    user_address  = message.text

    await message.answer(f"Спасибо! Ваш адрес: {user_address} записан.")
 
    update_user_address(message.from_user.id, message.text)

    await state.clear()





@deliver_router.callback_query(F.data == "confirm_address")
async def process_confirm_address(callback: types.CallbackQuery):
    await callback.message.answer("Отлично! Этот адрес сохранен для вашей доставки. ✨")
    
    # ОБЯЗАТЕЛЬНО: гасим "часики" (анимацию загрузки) на кнопке в Telegram
    await callback.answer()

@deliver_router.callback_query(F.data == "change_address")
async def process_change_address(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Хорошо, введите новый адрес доставки:")
    
    # Включаем машину состояний (FSM) на шаг адреса, чтобы бот ждал текст
    await state.set_state(DeliveryStates.waiting_for_address) 
    await callback.answer()    
    