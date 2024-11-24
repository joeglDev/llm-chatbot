from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

from Prompts import SYSTEM_PROMPT
from classes.CountryCodes import CountryCodes
from classes.NewsRetriever import NewsRetriever


class LLM:
    def __init__(self, model: str, country_code: CountryCodes):
        self.llm = OllamaLLM(model=model)
        self.country_code = country_code

    def get_completion(self):
        # Step 1: Get news data
        retriever = NewsRetriever()
        news_response = retriever.get_news(country_code=self.country_code)

        # Step 2: Define a prompt
        prompt_template = ChatPromptTemplate(
            [
                ("system", SYSTEM_PROMPT),
                (
                    "user",
                    "Please summarise the following news articles: {news_articles}",
                ),
            ]
        )

        prompt = prompt_template.invoke({"news_articles": news_response})

        # Step 3: Generate LLM response
        # TODO: format as pydantic object
        completion: str = self.llm.invoke(prompt)
        return completion
