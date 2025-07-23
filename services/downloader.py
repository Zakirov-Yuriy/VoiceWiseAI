# downloader.py

import os
import re
from uuid import uuid4
from aiogram.types import Message
import yt_dlp

DOWNLOAD_DIR = "temp"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


async def download_file(message: Message) -> str:
    file = None
    if message.document:
        file = message.document
    elif message.video:
        file = message.video
    elif message.audio:
        file = message.audio
    elif message.voice:
        file = message.voice

    file_id = file.file_id
    file_name = file.file_name or f"{uuid4()}.mp4"
    file_path = os.path.join(DOWNLOAD_DIR, file_name)

    await message.bot.download(file, destination=file_path)
    return file_path


def is_youtube_url(url: str) -> bool:
    pattern = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+"
    return bool(re.match(pattern, url))


async def download_youtube(url: str) -> str | None:
    try:
        # Обрабатываем shorts ссылки
        if "shorts" in url:
            video_id = url.split("/")[-1]
            url = f"https://www.youtube.com/watch?v={video_id}"

        ydl_opts = {
            'format': 'mp4',
            'cookies': 'cookies.txt',
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(id)s.%(ext)s'),
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_id = info_dict.get("id", None)
            if not video_id:
                print("[ERROR] video_id не найден.")
                return None

            file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp4")

        return file_path

    except Exception as e:
        print(f"[ERROR] Не удалось скачать видео: {e}")
        return None

