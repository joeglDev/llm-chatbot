import os
from typing import List

import torch
from playsound import playsound
from tortoise import api
import torchaudio
from tortoise.utils import audio


class TextToSpeech:
    def __init__(
        self, voice: str, sample_rate: int, sample_rate_reference: int
    ):  # voice = folder name
        self.tts = api.TextToSpeech(
            device="cuda" if torch.cuda.is_available() else "cpu"
        )
        self.path = os.path.dirname(os.path.abspath(__file__)) + "/../data/output.wav"
        self.voice = os.path.dirname(os.path.abspath(__file__)) + f"/voices/{voice}"
        self.sample_rate = sample_rate
        self.sample_rate_reference = sample_rate_reference

    def _split_text(self):
        pass

    def _get_audio_file_paths(self, dir_path: str) -> List[str]:
        path = os.path.abspath(dir_path)
        return [entry.path for entry in os.scandir(path) if entry.is_file()]

    def _clean_temp_files(self):
        try:
            os.remove(self.path)
        except FileNotFoundError:
            print("No preexisting audio file file to delete")

    def _generate_audio(self):
        clips_paths = self._get_audio_file_paths(
            self.voice
        )  # todo: find khajit audio samples
        ref_clips = [
            audio.load_audio(p, self.sample_rate_reference) for p in clips_paths
        ]
        audio_tensors = self.tts.tts_with_preset(
            "Hello there. My name is Captain Jean Luq Picard.",
            preset="ultra_fast",
            voice_samples=ref_clips,
        )
        torchaudio.save(
            src=audio_tensors[0], uri=self.path, sample_rate=self.sample_rate
        )  # try 20,000 and 25,000
        playsound(self.path)

    def run(self):
        self._clean_temp_files()
        self._generate_audio()


TextToSpeech(voice="pat", sample_rate=22_500, sample_rate_reference=22_050).run()
