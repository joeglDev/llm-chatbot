from tempfile import template

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
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
        format_instructions = ""  # placeholder for pydantic
        prompt = PromptTemplate(
            template="Answer the user query. \n {query}\n",
            input_variables=["query"],
            # partial_variables={"format_instructions": format_instructions},
        )
        query_template = PromptTemplate.from_template(SYSTEM_PROMPT)
        query = query_template.format(
            articles=news_response[
                0
            ]  # TODO: return all articles and process each as a separate async LLM call
        )

        # prompt = prompt_template.invoke({"news_articles": news_response})

        # Step 3: Generate LLM response
        # TODO: format as pydantic object
        # TODO: to ensure that each news article is accurate send each as a single LLM prompt and response async
        # completion: str = self.llm.invoke(prompt)
        chain = prompt | self.llm  # parser
        completion = chain.invoke(query)
        return completion
