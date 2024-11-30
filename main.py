from dataclasses import dataclass
from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from classes.CountryCodes import CountryCodes
from classes.Llm import LLM
from classes.TextToSpeech import TextToSpeech


@dataclass
class GetNewsResponse:
    text_summary: str


app = FastAPI()


@app.get("/")
def ping():
    return "pong"


@app.get("/news")
def get_news(country_code: CountryCodes, topic: str) -> GetNewsResponse:
    llm = LLM(model="mistral", country_code=country_code, topic=topic)
    completion = llm.get_completion()
    response = GetNewsResponse(text_summary=completion)
    return response


@app.get("/news/audio")
def get_news(country_code: CountryCodes, topic: str) -> StreamingResponse:
    llm_service = LLM(model="mistral", country_code=country_code, topic=topic)
    completions = llm_service.get_completion()
    completions_str = "Next article: ".join(completions)

    tts_service = TextToSpeech(
        tts_model="tts_models/multilingual/multi-dataset/xtts_v2",
        speaker="Baldur Sanjin",
        language="en",
    )
    audio_stream = tts_service.run(completions_str)
    file_name = f"{datetime.today().strftime('%Y-%m-%d')}-news"
    headers = {"Content-Disposition": f'attachment; filename="{file_name}.wav"'}

    response = StreamingResponse(
        content=audio_stream, media_type="audio/wav", headers=headers
    )
    return response
