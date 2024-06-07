from duckduckgo_search import DDGS
from openai import OpenAI
import json
import os
from client import RestClient
from exa_py import Exa

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
exa = Exa(api_key="5ff4f2f8-e37e-4902-9c3c-0c77eaeb7327")
class companyCompetitors:

    def competitorsFinder(self,company_name,source):
        if source == 'DataforSEO':
            client = RestClient("kwadwo.adu@plyolab.com", "b13fca3dc310b90f")
            post_data = dict()
            post_data[len(post_data)] = dict(
                target=company_name,
                location_name="United States",
                language_name="English",
                exclude_top_domains=True,
                filters = [
                ["domain","not_regex","(tiktok.com|stackoverflow.com|go.dev|jetbrains.com|github.com|indeed.com|microsoft.com|apple.com|forbes.com|pinterest.com|amazon.com|google.com|facebook.com|wordpress.com|medium.com|quora.com|reddit.com|youtube.com|ebay.com|uol.com.br|instagram.com|twitter.com|linkedin.com|slideshare.net)"]],
                    limit=10
                )
            response = client.post("/v3/dataforseo_labs/google/competitors_domain/live", post_data)
            if response["status_code"] == 20000:
                try:
                    domain_links = []

                    for task in response['tasks']:
                        for item in task['result'][0]['items']:
                            domain_links.append(item['domain'])

                    return {'Competitor':domain_links}
                except:
                    return {'Competitor':[]}
            else:
                return {'Competitor':[]}
        elif source == 'Exa':
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
                return {'Competitor':[]}

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