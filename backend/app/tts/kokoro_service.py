from kokoro import KPipeline
import wave
import numpy as np
import uuid
import os


class KokoroService:

    def __init__(self):

        self.pipeline = KPipeline(lang_code="a")

        os.makedirs("audio", exist_ok=True)

    def generate_audio(self, text: str):

        filename = f"{uuid.uuid4()}.wav"

        filepath = os.path.join("audio", filename)

        generator = self.pipeline(
            text,
            voice="af_heart",
        )

        with wave.open(filepath, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(24000)

            for _, _, audio in generator:
                if audio is None:
                    continue

                audio_np = audio.numpy() if hasattr(audio, "numpy") else np.asarray(audio)
                if np.issubdtype(audio_np.dtype, np.floating):
                    audio_int16 = (audio_np * 32767).astype(np.int16)
                else:
                    audio_int16 = audio_np.astype(np.int16)

                wav_file.writeframes(audio_int16.tobytes())

        return filename


tts = KokoroService()