import os
import json
from dataclasses import dataclass
from typing import List, Dict, Optional

import requests
from dotenv import load_dotenv

from classes.CountryCodes import CountryCodes


@dataclass
class NewsArticle:
    id: int
    title: str
    text: str
    summary: str
    url: str
    image: str | None
    video: str | None
    publish_date: str
    author: str
    authors: List[str]
    sentiment: float
    language: str
    source_country: str
    category: Optional[str] = None


class NewsRetriever:
    def _convert_articles_to_dataclass(self, article: Dict) -> NewsArticle:
        return NewsArticle(**article)

    def get_news(self, country_code: CountryCodes) -> List[NewsArticle]:
        load_dotenv()
        API_KEY = os.environ.get("API_KEY")
        search_url = f"https://api.worldnewsapi.com/search-news?text=climate+change&source-country={country_code.value}&language=en" #todo: add a topic
        headers = {"x-api-key": API_KEY}

        response = requests.get(search_url, headers=headers)
        response.raise_for_status()

        search_results = json.loads(response.text)
        raw_articles = search_results["news"]

        converted_articles = [
            self._convert_articles_to_dataclass(article) for article in raw_articles
        ]
        return converted_articles
