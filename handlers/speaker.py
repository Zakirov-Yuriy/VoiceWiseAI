from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import os
from services.downloader import is_youtube_url, download_youtube
from services.extractor import extract_audio

from services.progress import ProgressManager
from utils.splitter import split_text

router = Router()

@router.message(F.text)
async def handle_speaker_youtube(message: Message, state: FSMContext):
    if message.text.strip() != "/спикеры":
        return  # Пропускаем другие команды

    await message.answer("🔗 Пришли ссылку на YouTube-видео для распознавания спикеров.")
    await state.set_state("waiting_for_speaker_video")

@router.message(F.text & F.state == "waiting_for_speaker_video")
async def process_speaker_video(message: Message, state: FSMContext):
    text = message.text.strip()

    if not is_youtube_url(text):
        await message.answer("❌ Это не похоже на YouTube-ссылку.")
        return

    progress = ProgressManager(message)
    await progress.update(5, "📥 Скачиваю видео...")

    file_path = await download_youtube(text)
    if not file_path:
        await message.answer("❌ Не удалось скачать видео.")
        return

    await progress.update(25, "🎵 Извлекаю аудио...")
    audio_path = extract_audio(file_path)

    await progress.update(50, "🧠 Отправляю на микросервис спикеров...")
    transcript = diarize_audio(audio_path)

    await progress.update(90, "📄 Разбиваю текст...")
    chunks = split_text(transcript)

    await progress.update(100, "✅ Готово! Отправляю результат...")

    for i, part in enumerate(chunks, start=1):
        await message.answer(f"📄 Часть {i}:\n{part}")

    os.remove(file_path)
    os.remove(audio_path)
    await state.clear()
