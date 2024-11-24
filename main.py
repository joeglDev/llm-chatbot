from dataclasses import dataclass

from fastapi import FastAPI

from classes.CountryCodes import CountryCodes
from classes.Llm import LLM


@dataclass
class GetNewsResponse:
    text_summary: str


app = FastAPI()


@app.get("/")
def ping():
    return "pong"


@app.get("/news")
def get_news(country_code: CountryCodes):
    llm = LLM(model="mistral", country_code=country_code)
    completion = llm.get_completion()
    response = GetNewsResponse(text_summary=completion)
    return response
