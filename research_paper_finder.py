from duckduckgo_search import DDGS
from openai import OpenAI
import json
import os
import time

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class researcher:

    def findRelativePapers(self,company_name):
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
        company_desc = response.choices[0].message.content

        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": ("You are Researcher Relevant Paper"
                                            "You are going to have company description and understand business"
                                            "When you create example search query it's going to use on academic websites that why you have to create queries according that"
                                            "You have to create google search query for relevant search paper about company use"
                                            "Response in JSON format"
                        "Provide your answer in JSON structure like this {'Example Query':['List Of Query']}")},
                {"role":"assistant","content": f"Here is company description: {company_desc}"},
                {"role": "user", "content": "I need to find research paper company use and I need search query"},
                
            ]
        )

        res = json.loads(response.choices[0].message.content)
        res_list = list()
        
        for item in res['Example Query']:
            time.sleep(1)
            results = DDGS().text(item, max_results=5)
            res_list.append(results)

        one_dim_list = [item for alt_liste in res_list for item in alt_liste]


        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": ("You are expert assistant"
                                            "Your job find most relevant research paper about company you given"
                                            "Understand every result you given and retrive to user most relevant academic research description and website link"
                                            "Give user list of all relevant research paper results"
                                            "Response in JSON format"
                        "Provide your answer in JSON structure like this {['Research Description':'Research description you find','Research Link':'Research Link you find'],...}"
                                            )},
                {"role":"assistant","content": f"Here is company description: {company_desc} and Here is all research queries results from google search: {one_dim_list}"},
                {"role": "user", "content": "I need to find research paper company use and I need search query"},
                
            ]
        )

        res = json.loads(response.choices[0].message.content)
        return res

