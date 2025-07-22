# services/extractor.py
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip


def extract_audio(file_path: str) -> str:
    audio_path = file_path + ".wav"
    try:
        if file_path.endswith(".mp3") or file_path.endswith(".wav"):
            # уже аудио
            os.rename(file_path, audio_path)
        else:
            video = VideoFileClip(file_path)
            video.audio.write_audiofile(audio_path)
    except Exception as e:
        print(f"Ошибка при извлечении аудио: {e}")
    return audio_path
