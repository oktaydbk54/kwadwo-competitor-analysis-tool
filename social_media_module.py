from duckduckgo_search import DDGS
from openai import OpenAI
from dotenv import load_dotenv
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class social_Links:

    def findSocialLinks(self,company_name,model_choice):

        query = f"{company_name} Social Media Links"
        results = DDGS().text(query, max_results=20)

        response = client.chat.completions.create(
        model=model_choice,
        messages=[
            {"role": "system", "content": (f"""
                    You are an expert Social media link finder.
                    You must thoroughly read and examine the information given to you.
                    As a result of the information given to you, I want you to list all the social media links of the company.
                    Your job is just to find and rotate links of social media platforms.
                    You need to return one link from each social media platform. 
                    You cannot send 2 different extensions from the same link.
                    Your job is to do research on company {company_name}. You should never, ever use or write any information other than company {company_name}. You can never, ever exceed this rule.
                    You have no other task other than finding Social Media links.""")},
            {"role":"assistant","content": f"Here is all Company Social Media Search Results: {results}"},
            {"role": "user", "content": f"As a result of the information given to you, I want you to give me all social media links about company {company_name}"},
            
            ]
        )
        return response.choices[0].message.content