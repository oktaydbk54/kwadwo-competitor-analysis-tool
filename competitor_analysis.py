from duckduckgo_search import DDGS
from openai import OpenAI
import json
import os
from client import RestClient
from exa_py import Exa

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
exa = Exa(api_key="5ff4f2f8-e37e-4902-9c3c-0c77eaeb7327")
class companyCompetitors:

    def competitorsFinder(self,company_name,source,model_choice):
        if source == 'ChatGPT':
            try:
                query_list = [f'{company_name} competitors',f'{company_name} alternatives']
                all_results = list()
                for item in query_list:    
                    results = DDGS().text(item, max_results=7)
                    all_results.append(results)

                    response = client.chat.completions.create(
                        model=model_choice,
                        response_format={ "type": "json_object" },
                        messages=[
                            {"role": "system", "content": ("Your task is to identify competing companies and respond as json."
                                                        "You need to thoroughly examine and analyze the data given to you."
                                                    f"It is your job to find competing companies' sites for company {company_name}."
                                                        "All you have to do is to write down the sites of all your rival companies in a list after making the necessary analysis and review."
                                                        "You only need to return the links of rival companies. You are expected to return the links of the rival companies you find in the descriptions in the body section."
                                                        "I want you to examine the explanations given to you and get the links of the competing companies you find there. You should not return a link with an extension from another site."
                                                        "Your task is only to return the links of the competing companies you find. You cannot return the name of a rival company within the extension of another site. For example: Google.com company's competitor website link is apple.com."
                                                        "The rival company you find cannot be an extension of another website. Do not exceed this rule. apple.com = correct/ cnbc.com/apple.com = wrong format."
                                                        "You only need to return competitor company links to the user. You cannot return any other data."
                                                        "You can never go beyond the above rules."
                                                        "Response in JSON format"
                                "Provide your answer in JSON structure like this {'Competitor': ['<Company Link>','<Company Link>'...]")},
                            {"role":"assistant","content": f"Here is all Google Company Search Results: {all_results}"},
                            {"role": "user", "content": f"I want you to give me links to competing companies for company {company_name}."},
                            
                        ]
                        )
                res = json.loads(response.choices[0].message.content)
                return res
            except:
                return [{'Competitor':[]}]
        if source == 'Exa':
            try:
                domain_links = list()
                result = exa.find_similar(
                company_name,
                num_results=10
                )
                res = result.results
                for item in res:
                    domain_links.append(item.url)
                return {'Competitor':domain_links}
            except:
                return [{'Competitor':[]}]

    def targetCompetitorAnalysis(self,company_name,target_company,model_choice):
        results = DDGS().text(f"Which company is better {company_name} or {target_company}", max_results=30)
        response = client.chat.completions.create(
            model=model_choice,
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": ("You are assistant"
                                            "Your task make analysis "
                                            "You have to compare which company is better for your task."
                                            "You need to thoroughly compare the information you have obtained and write a small report to the user."
                                            "Response in JSON format"
                    "Provide your answer in JSON structure like this {'Overview': 'Overview Results','Key Comparisons':'Key Comparisons Results','Features and Capabilities':'Features and Capabilities Results','Conclusion':'Conclusion Results'}")},
                {"role":"assistant","content": f"Here is all Google Company Search Results: {results}"},
                {"role": "user", "content": "Based on the google search give me analysis results which company better? "},
                
            ]
            )
        res = json.loads(response.choices[0].message.content)
        return res