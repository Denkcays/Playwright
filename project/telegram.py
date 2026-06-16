from aiogram import Bot, Dispatcher
from headers.routers import router
from dotenv import load_dotenv
from os import getenv
import asyncio

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
dp.include_router(router)

async def main():
    print("Bot start working")
    bot = Bot(token = TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())