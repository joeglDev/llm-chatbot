# LLM new retriever

## Summary

Backend service which extracts news articles from an external api and parses through an LLM to provide opinion.

- Current news api source: https://worldnewsapi.com/docs/top-news/

## Quickstart
- Install dependencies with poetry 
- `fastapi dev main.py`

## API documentation

#### **GET** /
- **Description:** Ping route to check if the API server is running.
- **Response:** Returns a string "pong".

#### **GET** /news
- **Description:** Fetches news articles based on the provided country code and topic.
- **Parameters:**
  - `country_code` (CountryCodes): The ISO-3166 alpha-2 country code.
  - `topic` (str): The desired news topic.
- **Response:** Returns a `GetNewsResponse` object with the text summary of the article.

#### **GET** /news/audio
- **Description:** Fetches news articles based on the provided country code and topic in an audio format.
- **Parameters:**
  - `country_code` (CountryCodes): The ISO-3166 alpha-2 country code.
  - `topic` (str): The desired news topic.
- **Response:** Returns a streaming response with the audio file in WAV format.


## Todo
- use pydantic to format LLM responses
- streaming endpoint

