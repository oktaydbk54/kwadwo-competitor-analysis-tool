from duckduckgo_search import DDGS
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


class companyDescription:

    def createDescription(self,company_name,model_choice):
        
        # query_list = [f'{company_name} overview',f'{company_name} Features',f'{company_name} Pricing model']
        
        # for item in query_list:
        results_overview = DDGS().text(f'{company_name} overview', max_results=10)
            # search_results.append(results)
        
        response_overview = client.chat.completions.create(
            model=model_choice,
            response_format= { 'type': "json_object" },
            messages=[
                {"role": "system", "content": ("Your task is to write a short description for the Company the user has researched. "
                                               "Your job is to explain things clearly to users."
                                               "You have to find the relevant information for each title within the researched company and then write the desired description in JSON."
                                               "Never rush this process."
                                               "You are an expert researcher"
                                            
                                            "Finally, after reading the information, I want you to give me a reference link."
                                            "You should response in JSON format"
    "Provide your answer in JSON structure like this {'Company Overview':'<Company Overview Description>','References':'<References you found>'}")},
                {"role":"assistant","content": f"Here is all Google Company Search Results: {results_overview}"},
                {"role": "user", "content": "Please write a 3-4 sentence description of the company based on the information provided in the search results."},
                
            ]
        )

        result_overview = json.loads(response_overview.choices[0].message.content)

        #### features

        results_features = DDGS().text(f'{company_name} features', max_results=10)

        response_feature = client.chat.completions.create(
            model="gpt-4o",
            response_format= { 'type': "json_object" },
            messages=[
                {"role": "system", "content": ("Your task is to write a short description for the Company the user has researched. "
                                               "Your job is to explain things clearly to users."
                                               "You have to find the relevant information for each title within the researched company and then write the desired description in JSON."
                                               "Never rush this process."
                                               "You are an expert researcher"
                                            
                                            "Finally, after reading the information, I want you to give me a reference link."
                                            "You should response in JSON format"
    "Provide your answer in JSON structure like this {'Company Features':'<Company Features you found>','References':'<References you found>'}")},
                {"role":"assistant","content": f"Here is all Google Company Search Results: {results_features}"},
                {"role": "user", "content": "Please write a Feature of the company based on the information provided in the search results."},
                
            ]
        )
        result_features= json.loads(response_feature.choices[0].message.content)

        #### Pricing

        results_pricing = DDGS().text(f'{company_name} pricing model', max_results=10)

        response_pricing = client.chat.completions.create(
            model="gpt-4o",
            response_format= { 'type': "json_object" },
            messages=[
                {"role": "system", "content": ("Your task is to write a short description for the Company the user has researched. "
                                               "Your job is to explain things clearly to users."
                                               "You have to find the relevant information for each title within the researched company and then write the desired description in JSON."
                                               "Never rush this process."
                                               "You are an expert researcher"
                                            
                                            "Finally, after reading the information, I want you to give me a reference link."
                                            "You should response in JSON format"
    "Provide your answer in JSON structure like this {'Company Pricing':'<Company Pricing you found>','References':'<References you found>'}")},
                {"role":"assistant","content": f"Here is all Search Results: {results_pricing}"},
                {"role": "user", "content": "Please write a Pricing model of the company based on the information provided in the search results."},
                
            ]
        )
        result_pricing = json.loads(response_pricing.choices[0].message.content)

        all_results = {
            'Overview':result_overview,
            'Features':result_features,
            'Pricing':result_pricing
        }
        print(result_pricing)
        # print()
        # print(resul)
        # print()
        # print(re)
        return all_results


