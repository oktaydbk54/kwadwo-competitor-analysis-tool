from duckduckgo_search import DDGS
from openai import OpenAI
from dotenv import load_dotenv
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class valuePro:

    def find_values(self,company_name):
        
        query_list = [f'{company_name} Company vs competitors',f'{company_name} Company competitive advantages',f'{company_name} Company market position compared to rivals']
        all_results = list()
        for item in query_list:
            results = DDGS().text(item, max_results=10)
            all_results.append(results)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": (f"""
                        You are a research assistant.
                        You need to read the information given to you carefully and in detail.
                        After reviewing all the information, you need to list these aspects to the user why this company should be preferred.
                        The only purpose of what you print is to explain to the customer why this company should be preferred.
                        Your task is to point out the differences between company {company_name} and other companies and explain why company {company_name} is better.
                        You need to use simple language that the user can understand.""")},
                {"role":"assistant","content": f"Here is all Search Results: {all_results}"},
                {"role": "user", "content": f"As a result of the information given to you, I want you to give me all advantages about company"},
                
            ]
        )
        return response.choices[0].message.content