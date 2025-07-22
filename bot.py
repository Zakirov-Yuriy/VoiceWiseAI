# bot.py
from aiogram import Dispatcher
from handlers.transcribe import router as transcribe_router

def register_handlers(dp: Dispatcher):
    dp.include_router(transcribe_router)

