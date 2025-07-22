# Это будет обработчик

# handlers/transcribe.py
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext

from services.downloader import download_file
from services.extractor import extract_audio
from services.transcriber import transcribe_audio
from services.progress import ProgressManager
from utils.splitter import split_text
# handlers/transcribe.py (добавить сверху)
from services.downloader import is_youtube_url, download_youtube


import os
import uuid

router = Router()


@router.message(F.text)
async def handle_youtube(message: Message, state: FSMContext):
    text = message.text.strip()

    if not is_youtube_url(text):
        return  # не YouTube, не обрабатываем

    progress = ProgressManager(message)
    await progress.update(5, "🔗 Скачиваю YouTube видео...")

    file_path = await download_youtube(text)
    if not file_path:
        await message.answer("❌ Не удалось скачать видео.")
        return

    await progress.update(25, "🎵 Извлекаю аудио...")
    audio_path = extract_audio(file_path)  # здесь убираем await, функция синхронная

    await progress.update(40, "🧠 Транскрибирую...")
    transcript = await transcribe_audio(audio_path, progress)

    await progress.update(90, "📄 Разбиваю текст...")
    chunks = split_text(transcript)

    await progress.update(100, "✅ Готово! Отправляю результат...")

    for i, part in enumerate(chunks, start=1):
        await message.answer(f"📄 Часть {i}:\n{part}")

    os.remove(file_path)
    os.remove(audio_path)
