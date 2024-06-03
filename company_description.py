from duckduckgo_search import DDGS
from openai import OpenAI
from dotenv import load_dotenv
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


class companyDescription:

    def createDescription(self,company_name):

        results = DDGS().text(company_name, max_results=15)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": ("Your task is to write a short 3-4 sentence description for the Company the user has researched. "
                                            "I want you to read and research the explanations given to you in detail."
                                            "I want you to use whatever information is most useful to the user."
                                            "Finally, after reading the information, I want you to give me a reference link.")},
                {"role":"assistant","content": f"Here is all Google Company Search Results: {results}"},
                {"role": "user", "content": "Please write a 3-4 sentence description of the company based on the information provided in the search results."},
                
            ]
        )
        return response.choices[0].message.content



