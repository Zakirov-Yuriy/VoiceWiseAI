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
import asyncio

router = Router()

MAX_LENGTH = 4000
semaphore = asyncio.Semaphore(4)  # максимум 3 параллельных задачи


@router.message(F.text)
async def handle_youtube(message: Message, state: FSMContext):
    text = message.text.strip()

    if not is_youtube_url(text):
        return

    progress = ProgressManager(message)
    await progress.update(5, "🔗 Скачиваю YouTube видео...")

    file_path = await download_youtube(text)
    print(f"[DEBUG] file_path = {file_path}")
    if not file_path:
        await message.answer("❌ Не удалось скачать видео.")
        return

    await progress.update(25, "🎵 Извлекаю аудио...")
    audio_path = extract_audio(file_path)

    await progress.update(30, "✂️ Разбиваю аудио на части...")
    audio_chunks = split_audio(audio_path, chunk_length_ms=5 * 60 * 1000)  # 5 минут

    full_transcript = ""

    # Создаём корутину для транскрипции с прогрессом
    async def process_chunk(idx, chunk_path, total_chunks):
        await progress.update(30 + int(60 * idx / total_chunks), f"🧠 Транскрибирую часть {idx}/{total_chunks}...")
        text = await transcribe_audio(chunk_path, progress)
        try:
            os.remove(chunk_path)
        except Exception:
            pass
        return text

    async def safe_process_chunk(*args, **kwargs):
        async with semaphore:
            return await process_chunk(*args, **kwargs)

    # Параллельно обрабатываем все куски
    tasks = [safe_process_chunk(idx, path, len(audio_chunks)) for idx, path in enumerate(audio_chunks, start=1)]
    results = await asyncio.gather(*tasks)

    full_transcript = "\n".join(results)


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