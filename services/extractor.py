# services/extractor.py
import os
from moviepy.video.io.VideoFileClip import VideoFileClip



def extract_audio(file_path: str) -> str:
    audio_path = file_path + ".wav"
    try:
        if file_path.endswith(".mp3") or file_path.endswith(".wav"):
            # Если уже аудиофайл — просто переименовываем
            os.rename(file_path, audio_path)
        else:
            # Извлекаем аудио из видео
            video = VideoFileClip(file_path)
            audio = video.audio
            audio.write_audiofile(audio_path)
            audio.close()   # 🔑 Закрываем аудио-объект
            video.close()   # 🔑 Закрываем видео-объект
    except Exception as e:
        print(f"Ошибка при извлечении аудио: {e}")
    return audio_path
