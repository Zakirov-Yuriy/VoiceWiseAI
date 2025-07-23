# services/transcriber.py

import os
import mimetypes
import aiohttp
import traceback

API_URL = os.getenv("LOCAL_TRANSCRIBE_API", "http://localhost:8000/transcribe")  # локальный API

def get_mime_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or "application/octet-stream"


async def transcribe_audio(audio_path: str, progress=None) -> str:
    if progress:
        await progress.update(50, "📡 Отправка на локальный API...")

    mime_type = get_mime_type(audio_path)
    file_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
    print(f"[transcribe_audio] Размер аудиофайла: {file_size_mb:.2f} МБ")

    try:
        timeout = aiohttp.ClientTimeout(total=300)  # 5 минут
        async with aiohttp.ClientSession(timeout=timeout) as session:

            with open(audio_path, "rb") as f:
                form = aiohttp.FormData()
                form.add_field(
                    name="file",
                    value=f,
                    filename=os.path.basename(audio_path),
                    content_type=mime_type
                )

                print("[transcribe_audio] Начинаю отправку файла в API...")
                async with session.post(API_URL, data=form) as resp:
                    print(f"[transcribe_audio] Ответ от API: {resp.status}")

                    if resp.status != 200:
                        text = await resp.text()
                        return f"❌ Ошибка API: {resp.status} — {text}"

                    data = await resp.json()

                    if "text" in data:
                        transcript = data["text"]
                        print(f"[transcribe_audio] Текст получен, длина: {len(transcript)} символов")
                        if progress:
                            await progress.update(80, "📋 Распознавание завершено.")
                        return transcript

                    return "❌ Ответ без текста"

    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"[transcribe_audio] Ошибка подключения к API:\n{error_trace}")
        return f"❌ Ошибка подключения к API: {error_trace}"
