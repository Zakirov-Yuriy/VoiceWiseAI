# transcribe.py Это будет обработчик

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
from services.audio_splitter import split_audio  # Импортируем

import traceback
import os
import uuid

router = Router()

MAX_LENGTH = 4000


@router.message(F.text)
async def handle_youtube(message: Message, state: FSMContext):
    text = message.text.strip()

    if not is_youtube_url(text):
        return

    progress = ProgressManager(message)
    await progress.update(5, "🔗 Скачиваю YouTube видео...")

    file_path = await download_youtube(text)
    if not file_path:
        await message.answer("❌ Не удалось скачать видео.")
        return

    await progress.update(25, "🎵 Извлекаю аудио...")
    audio_path = extract_audio(file_path)

    await progress.update(30, "✂️ Разбиваю аудио на части...")
    audio_chunks = split_audio(audio_path, chunk_length_ms=5 * 60 * 1000)  # 5 минут

    full_transcript = ""

    for idx, chunk_path in enumerate(audio_chunks, start=1):
        await progress.update(30 + int(60 * idx / len(audio_chunks)), f"🧠 Транскрибирую часть {idx}/{len(audio_chunks)}...")
        chunk_text = await transcribe_audio(chunk_path, progress)
        full_transcript += chunk_text + "\n"

        # Можно удалить обработанный кусок, если не нужен
        try:
            os.remove(chunk_path)
        except Exception:
            pass

    await progress.update(90, "📄 Разбиваю текст на части...")

    chunks = split_text(full_transcript)

    await progress.update(100, "✅ Готово! Отправляю результат...")

    try:
        for i, part in enumerate(chunks, start=1):
            await message.answer(f"📄 Часть {i}:\n{part}")
    except Exception as e:
        print(f"❌ Ошибка отправки в Telegram: {e}")
        await message.answer("❌ Ошибка при отправке результата.")

    try:
        os.remove(file_path)
        os.remove(audio_path)
    except Exception:
        pass