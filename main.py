import asyncio, aiogram, os, dotenv
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from database import init_db
from handlers.menu import menu_router
from handlers.cabinet import users_router
from handlers.deliver import deliver_router

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    exit("Ошибка: Токен бота не найден в файле .env!")
else:
    print("token is safe")

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(menu_router)
dp.include_router(users_router)
dp.include_router(deliver_router)



async def main():
    init_db()
    print("Бот для продажи тортиков успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())