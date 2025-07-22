# handlers/base.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram import Dispatcher

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer("👋 Привет! Я бот для транскрибации видео и аудио в текст.\n"
                         "📥 Просто пришли мне аудио/видео файл или YouTube-ссылку.")

@router.message(F.text == "/help")
async def cmd_help(message: Message):
    await message.answer("🛠 Возможности:\n"
                         "- Поддержка аудио/видео файлов\n"
                         "- Поддержка YouTube-ссылок\n"
                         "- Распознавание спикеров\n"
                         "- Прогрессбар с процентами\n"
                         "📩 Отправь файл или ссылку, и я начну работу!")

def register_base(dp: Dispatcher):
    dp.include_router(router)
