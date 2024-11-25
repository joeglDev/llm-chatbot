import os
from typing import List

import requests
from dotenv import load_dotenv
from requests import Response

from classes.CountryCodes import CountryCodes


class NewsRetriever:
    def get_news(self, country_code: CountryCodes) -> str:
        load_dotenv()
        API_KEY = os.environ.get("API_KEY")
        headers = {"x-api-key": API_KEY}
        url = f"https://newsapi.org/v2/top-headlines?country={country_code.value}"

        res = requests.get(url, headers=headers)

        # TODO: model as dataclass
        res_as_list = res.json()

        articles = ""
        for article in res_as_list["articles"]:
            source = article["source"]["id"]
            description = article["description"]
            articles = articles + f"{source}: {description} \n"

        return articles
