# services/transcriber.py
import requests
import os
from config import HF_API_TOKEN
import mimetypes

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"

def get_mime_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or "application/octet-stream"

headers_base = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
}

async def transcribe_audio(audio_path: str, progress=None) -> str:
    if progress:
        await progress.update(50, "📡 Отправка в HuggingFace...")

    mime_type = get_mime_type(audio_path)
    headers = headers_base.copy()
    headers["Content-Type"] = mime_type

    with open(audio_path, "rb") as f:
        audio_bytes = f.read()

    response = requests.post(API_URL, headers=headers, data=audio_bytes)

    if response.status_code != 200:
        print("Ошибка:", response.status_code, response.text)
        return "❌ Ошибка при транскрибации"

    result = response.json()
    if isinstance(result, dict) and "text" in result:
        if progress:
            await progress.update(80, "📋 Распознавание завершено.")
        return result["text"]
    else:
        return "❌ Текст не получен"
