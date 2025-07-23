# bot.py
from aiogram import Dispatcher
from handlers.transcribe import router as transcribe_router
from handlers.speaker import router as speaker_router

def register_handlers(dp: Dispatcher):
    dp.include_router(transcribe_router)
    dp.include_router(speaker_router)

