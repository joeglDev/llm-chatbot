import asyncio
from tempfile import template
from typing import List, Coroutine

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_ollama.llms import OllamaLLM

from Prompts import SYSTEM_PROMPT
from classes.CountryCodes import CountryCodes
from classes.NewsRetriever import NewsRetriever, NewsArticle


class LLM:
    def __init__(self, model: str, country_code: CountryCodes, topic: str):
        self.llm = OllamaLLM(model=model)
        self.country_code = country_code
        self.topic = topic

    async def _get_completions_async(self, articles: List[NewsArticle]) -> List[str]:
        completions: List[Coroutine] = []

        # Step 2: Define a prompt
        for article in articles:
            format_instructions = ""  # placeholder for pydantic
            prompt = PromptTemplate(
                template="Answer the user query. \n {query}\n",
                input_variables=["query"],
                # partial_variables={"format_instructions": format_instructions},
            )
            query_template = PromptTemplate.from_template(SYSTEM_PROMPT)
            query = query_template.format(articles=article)

            # prompt = prompt_template.invoke({"news_articles": news_response})

            # Step 3: Generate LLM responses
            # TODO: format as pydantic object
            # completion: str = self.llm.invoke(prompt)

            chain = prompt | self.llm  # parser
            completions.append(chain.ainvoke(query))

        # Step 4: resolve coroutines and return
        awaited_completions: List[str] = await asyncio.gather(*completions)
        return awaited_completions

    def get_completion(self):
        # Step 1: Get news data
        retriever = NewsRetriever()
        news_responses = retriever.get_news(
            country_code=self.country_code, topic=self.topic
        )
        sliced_news_responses = news_responses[:2]
        print(sliced_news_responses)

        completions = asyncio.run(
            self._get_completions_async(sliced_news_responses)
        )  # todo: expand slice to more articles
        return completions
