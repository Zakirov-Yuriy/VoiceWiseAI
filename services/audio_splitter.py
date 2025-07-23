from pydub import AudioSegment
import os

def split_audio(audio_path: str, chunk_length_ms: int = 5 * 60 * 1000) -> list[str]:
    """
    Разбивает аудио файл на части длиной chunk_length_ms (по умолчанию 5 минут)
    Возвращает список путей к новым аудио файлам
    """
    audio = AudioSegment.from_file(audio_path)
    duration_ms = len(audio)

    chunks = []
    base_name, ext = os.path.splitext(audio_path)

    for i, start_ms in enumerate(range(0, duration_ms, chunk_length_ms)):
        end_ms = min(start_ms + chunk_length_ms, duration_ms)
        chunk = audio[start_ms:end_ms]

        chunk_filename = f"{base_name}_part{i+1}{ext}"
        chunk.export(chunk_filename, format=ext.replace(".", ""))
        chunks.append(chunk_filename)

    return chunks
