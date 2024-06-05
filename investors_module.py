from duckduckgo_search import DDGS
from openai import OpenAI
from dotenv import load_dotenv
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class Inverstors:

    def investors_values(self,company_name):

        query_list = [f'{company_name} Company investment history',f'{company_name} Company investors',f'{company_name} Investment Round',f'{company_name} Investment Amount']
        all_results = list()
        for item in query_list:
            results = DDGS().text(item, max_results=10)
            all_results.append(results)
        response = client.chat.completions.create(
            model="gpt-4o",
            # response_format= { 'type': "json_object" },
            messages=[
                {"role": "system", "content": ("Your job is to thoroughly read and understand the information given to you."
                                            "In general, you only have to provide information about the investment the company received. You cannot touch on other topics."
                                            "Your job is to thoroughly evaluate the internet results and then compile a report for me using all the information related to the company's investment."
                                            "You should always choose an easily understandable language."
        #                                     "You should response in JSON format"
        # "Provide your answer in JSON structure like this {'Investors':'<Investors you found>','Description':'<Description you found>','References':'<References you found>'}"
        )},
                {"role":"assistant","content": f"Here is all Company Invesment Search Results: {all_results}"},
                {"role": "user", "content": f"As a result of the information given to you, I want you to give me conclusions about the investment received by company {company_name}"},
                
            ]
        )
        return response.choices[0].message.content#json.loads(response.choices[0].message.content)