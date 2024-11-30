import os

import torch
from TTS.api import TTS
from playsound import playsound

from tests.data.mock_llm_response import MOCK_LLM_RESPONSE

# todo: integrate into llm system and return audio file NOT text using a diff endpoint


class TextToSpeech:
    def __init__(self, tts_model: str, speaker: str, language: str):
        self.tts_model = tts_model
        self.speaker = speaker
        self.language = language
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts = TTS(self.tts_model).to(self.device)
        self.path = os.path.dirname(os.path.abspath(__file__)) + "/../data/output.wav"

    def _synthesise_speech(self, completion: str):
        # Run TTS
        # ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
        # Text to speech list of amplitude values as output
        print("Generating voice...")

        self.tts.tts_to_file(
            text=completion,
            file_path=self.path,
            speaker=self.speaker,
            language=self.language,
            split_sentences=True,
        )

    def _speak(self):
        """play audio from file"""

        print("Speaking...")
        playsound(self.path)

    def _clean_file(self):
        try:
            os.remove(self.path)
        except Exception:
            print("No preexisting audio file file to delete")

    def _read_file(self) -> bytes:
        chunk_size = 4096
        try:
            with open(self.path, "rb") as file:
                while True:
                    chunk = file.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
        except IOError as e:
            print(f"Error reading audio file: {e}")

    def run(self, completion: str):
        self._clean_file()
        self._synthesise_speech(completion)
        return self._read_file()
