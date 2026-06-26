from aiogram import Router, F, types
from keyboards import get_main_keyboard

deliver_router = Router()

@deliver_router.message(F.text == "deliver")
async def process_deliver(message: types.Message):
    # Текст, который увидит пользователь
    delivery_text = (
        "🚚 **Информация о доставке тортиков:**\n\n"
        "✨ Доставка по городу — 300 рублей.\n"
        "✨ При заказе от 3000 рублей — бесплатно!\n"
        "⏱️ Пожалуйста, делайте заказ минимум за 2-3 дня."
    )
    
    # Отправляем текст и прикрепляем главное меню обратно
    await message.answer(text=delivery_text, reply_markup=get_main_keyboard())