# services/speaker_diary.py

import requests



API_URL = "http://localhost:8000/diarize"  # Укажи URL своего микросервиса (или API AssemblyAI)
TIMEOUT = 600  # 10 минут

def diarize_audio(audio_path: str) -> str:
    with open(audio_path, "rb") as f:
        files = {"file": f}
        try:
            response = requests.post(API_URL, files=files, timeout=TIMEOUT)
            response.raise_for_status()
            return response.text  # Или response.json() если API возвращает JSON
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при отправке аудио на микросервис: {e}")
            return "Ошибка при распознавании спикеров"
