from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext 
from aiogram.types import Message
from aiogram import F, Router

deliver_router = Router()

class DeliveryStates(StatesGroup):
    waiting_for_address = State()



@deliver_router.message(F.text == "deliver")  
async def process_deliver(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, введите ваш адрес доставки:")

    await state.set_state(DeliveryStates.waiting_for_address) 



@deliver_router.message(DeliveryStates.waiting_for_address) 
async def process_deliver(message: Message, state: FSMContext):
    user_address  = message.text

    await message.answer(f"Спасибо! Ваш адрес: {user_address} записан.")

    await state.clear()
    