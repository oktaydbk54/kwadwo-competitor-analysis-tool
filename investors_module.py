from duckduckgo_search import DDGS
from openai import OpenAI
from dotenv import load_dotenv
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class Inverstors:

    def investors_values(self,company_name):

        query = f"{company_name} investment raised"
        
        results = DDGS().text(query, max_results=20)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": ("Your job is to thoroughly read and understand the information given to you."
                                            "In general, you only have to provide information about the investment the company received. You cannot touch on other topics."
                                            "Your job is to thoroughly evaluate the internet results and then compile a report for me using all the information related to the company's investment."
                                            "You should always choose an easily understandable language.")},
                {"role":"assistant","content": f"Here is all Company Invesment Search Results: {results}"},
                {"role": "user", "content": f"As a result of the information given to you, I want you to give me conclusions about the investment received by company {company_name}"},
                
            ]
        )
        return response.choices[0].message.content
