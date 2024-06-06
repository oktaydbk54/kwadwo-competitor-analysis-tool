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
        results_overview = DDGS().text(f"{company_name} General Information", max_results=5)
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
                                            f"Your job is to do research on company {company_name}. You should never, ever use or write any information other than company {company_name}. You can never, ever exceed this rule."
                                            "Finally, after reading the information, I want you to give me a reference link."
                                            "You should response in JSON format"
    "Provide your answer in JSON structure like this {'Company Overview':'<Company Overview Description>','References':'<References you found>'}")},
                {"role":"assistant","content": f"Here is all Google Company Search Results: {results_overview}"},
                {"role": "user", "content": f"You are searching assistant and I will give example document if it's about {company_name} Company I want you to create the most relevant parts for me"},
                
            ]
        )

        result_overview = json.loads(response_overview.choices[0].message.content)

        #### features

        results_features = DDGS().text(f"{company_name} features", max_results=5)

        response_feature = client.chat.completions.create(
            model=model_choice,
            response_format= { 'type': "json_object" },
            messages=[
                {"role": "system", "content": ("Your task is to write a short description for the Company the user has researched. "
                                               "Your job is to explain things clearly to users."
                                               "You have to find the relevant information for each title within the researched company and then write the desired description in JSON."
                                               "Never rush this process."
                                               "You are an expert researcher"
                                                f"Your job is to do research on company {company_name}. You should never, ever use or write any information other than company {company_name}. You can never, ever exceed this rule."
                                            "Finally, after reading the information, I want you to give me a reference link."
                                            "You should response in JSON format"
                                            "You can never output anything other than the JSON output example given to you. never ever."
    "Provide your answer in JSON structure like this {'Company Features':'<Company Features you found>','References':'<References you found>'}")},
                {"role":"assistant","content": f"Here is all Google Company Search Results: {results_features}"},
                {"role": "user", "content": f"You are searching assistant and I will give example document if it's about {company_name} Company I want you to create the most relevant parts for me"},
                
            ]
        )
        result_features= json.loads(response_feature.choices[0].message.content)

        #### Pricing

        results_pricing = DDGS().text(f"{company_name} pricing", max_results=5)

        response_pricing = client.chat.completions.create(
            model=model_choice,
            response_format= { 'type': "json_object" },
            messages=[
                {"role": "system", "content": ("Your task is to write a short description for the Company the user has researched. "
                                               "Your job is to explain things clearly to users."
                                               "You have to find the relevant information for each title within the researched company and then write the desired description in JSON."
                                               f"If the href value in the JSON given to you is related to the searched company {company_name} or belongs to another company, never evaluate those values."
                                               "You are an expert researcher"
                                                f"Your job is to do research on company {company_name}. You should never, ever use or write any information other than company {company_name}. You can never, ever exceed this rule."
                                            "Finally, after reading the information, I want you to give me a reference link."
                                            
                                            "You should response in JSON format"
    "Provide your answer in JSON structure like this {'Company Pricing':'<Company Pricing you found>','References':'<References you found>'}")},
                {"role":"assistant","content": f"Here is all Search Results: {results_pricing}"},
                {"role": "user", "content": f"You are searching assistant and I will give example document if it's about {company_name} Company I want you to create the most relevant parts for me.Please write a Pricing model of the company based on the information provided in the search results."},
                
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


