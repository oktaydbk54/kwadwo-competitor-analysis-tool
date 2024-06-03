from duckduckgo_search import DDGS
from openai import OpenAI
import json
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class companyCompetitors:

    def competitorsFinder(self,company_name):

        results = DDGS().text(f"{company_name} Alternatives, Competitors", max_results=20)
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": ("You are assistant"
                                            "Your task find competitors"
                                            "Response in JSON format"
                                            "Provide your answer in JSON structure like this {'Competitor':['List Of Competitors']}")},
                {"role":"assistant","content": f"Here is all Google Company Search Results: {results}"},
                {"role": "user", "content": f"Based on the google search I want you to find competitors of {company_name} company and give me a list"},    
            ]
            )
        res = json.loads(response.choices[0].message.content)
        return res

    def targetCompetitorAnalysis(self,company_name,target_company):
        results = DDGS().text(f"Which company is better {company_name} or {target_company}", max_results=30)


        response = client.chat.completions.create(
            model="gpt-4o",
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