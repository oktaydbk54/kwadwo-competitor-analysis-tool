from duckduckgo_search import DDGS
from openai import OpenAI
from dotenv import load_dotenv
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


class companyFounderDescription:

    def createDescription(self,company_name):
        query = f"{company_name} company founders"
        results = DDGS().text(query, max_results=20)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": ("Your job is to thoroughly read and understand the information given to you."
                                        "You have to give me as much information about the founders of the company as you can find in the given information, in order."
                                        "You should always choose an easily understandable language."
                                        "You only have to provide information about the founders of the company being investigated, you cannot touch on anything else.")},
            {"role":"assistant","content": f"Here is all Google Company Founders Search Results: {results}"},
            {"role": "user", "content": "Write me information about the founders of the company from the information given to you."},
            
        ]
        )
        return response.choices[0].message.content



