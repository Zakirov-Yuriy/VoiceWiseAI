import os

# ✅ Сохраняем cookies.txt из переменной окружения (если задана)
cookies = os.getenv("YT_COOKIES")
print(f"YT_COOKIES length: {len(cookies) if cookies else 'None'}")
print(f"YT_COOKIES preview:\n{cookies[:200]}")

if cookies:
    with open("cookies.txt", "w", encoding="utf-8") as f:
        f.write(cookies)
else:
    print("YT_COOKIES is empty")

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from bot import register_handlers

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    register_handlers(dp)

    print("🤖 Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
