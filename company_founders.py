from duckduckgo_search import DDGS
from openai import OpenAI
from dotenv import load_dotenv
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


class companyFounderDescription:

    def createDescription(self,company_name,model_choice):
        query_list = [f"'{company_name}' company founders",f"'{company_name}' founders information",f"'{company_name}' founders"]
        all_results = list()
        for item in query_list:
            results = DDGS().text(item, max_results=7)
            all_results.append(results)
        response = client.chat.completions.create(
            model=model_choice,
            
            messages=[
            {"role": "system", "content": ("Your job is to thoroughly read and understand the information given to you."
                                        "You have to give me as much information about the founders of the company as you can find in the given information, in order."
                                        "You should always choose an easily understandable language."
                                        "You must always leave a reference link at the end of the report you write. "
                                        f"Your job is to do research on company {company_name}. You should never, ever use or write any information other than company {company_name}. You can never, ever exceed this rule."
                                        f"You should create a report using information about company {company_name}. If you see a name or information outside Company {company_name}, you are advised to ignore it and never add it."
                                        "You only have to provide information about the founders of the company being investigated, you cannot touch on anything else.")},
            {"role":"assistant","content": f"Here is all Google {company_name} Founders Search Results: {all_results}"},
            {"role": "user", "content": f"You should create a report using information about company {company_name}. If you see a name or information outside Company {company_name}, you are advised to ignore it and never add it.Write me information about the founders of the company from the information given to you. You must always leave a reference link at the end of the report you write."},
            
        ]
        )

        return response.choices[0].message.content



