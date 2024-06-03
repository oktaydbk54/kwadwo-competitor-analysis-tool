from duckduckgo_search import DDGS
from openai import OpenAI
from dotenv import load_dotenv
import json
from client import RestClient
import os

client_openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


class domainAnalysis:

    def domain_rank_module(self,company_name):
        client = RestClient("kwadwo.adu@plyolab.com", "b13fca3dc310b90f")
        post_data = dict()
        post_data[len(post_data)] = dict(
            target=company_name,
            location_name="United States",
            language_name="English"    
        )
        response = client.post("/v3/dataforseo_labs/google/domain_rank_overview/live", post_data)
        if response["status_code"] == 20000:
            
            endpoint_desc = """Domain Rank Overview
            This endpoint will provide you with ranking and traffic data from organic and paid search for the specified domain. You will be able to review the domain ranking distribution in SERPs as well as estimated monthly traffic volume for both organic and paid results."""

            response = client_openai.chat.completions.create(
                model="gpt-4o",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": (""" 
                        You are an SEO expert. Your task is to interpret the JSON responses from SEO sites I use and report them to a client in a simple and understandable way.

                        Instructions:
                        1. Write a comment to the user in a clear and understandable manner.
                        2. Take your time to ensure accuracy in interpreting all values.
                        3. Create a report-style summary of the analysis results, focusing on Organic Search Overview and Paid Search Overview.
                        4. Perform a comprehensive domain analysis using the provided JSON file.
                        5. Your response should be in JSON format.

                        Ensure your response adheres to this format:
                        {
                            "Domain Analysis": "<Your Analysis Report>"
                        }""")},
                    {"role":"assistant","content": f"Here is Endpoint description: {endpoint_desc}, Here is JSON response: {response}"},
                    {"role": "user", "content": "I want you to perform a Domain Analysis for me by looking at the JSON file given to you."},
                    
                ]
            )
            result = json.loads(response.choices[0].message.content)
            return result
        else:
            return None
    
    def historical_rank_module(self,company_name):
        client = RestClient("kwadwo.adu@plyolab.com", "b13fca3dc310b90f")
        post_data = dict()
        post_data[len(post_data)] = dict(
            target=company_name,
            location_name="United States",
            language_name="English",
        )
        response = client.post("/v3/dataforseo_labs/google/historical_rank_overview/live", post_data)
        if response["status_code"] == 20000:
            
            endpoint_desc = """
            Historical Rank Overview
            This endpoint will provide you with historical data on rankings and traffic of the specified domain, such as domain ranking distribution in SERPs and estimated monthly traffic volume for both organic and paid results."""

            response = client_openai.chat.completions.create(
                model="gpt-4o",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": (""" 
                        You are an SEO expert
                        Your task is to interpret the JSON responses coming from some SEO sites I use as a source and I want you to report them to a client in a simple and understandable way.
                        You have to write a comment to the user in a simple and understandable way.
                        You should never rush during this process.
                        When reviewing your JSON response, you need to evaluate it in detail and make sure.
                        JSON contains the user's past rank overview information. Using this information you have to write an informative report to the user.
                        You have to understand and interpret all the values ​​​​well.
                        You should response in JSON format
                        Provide Json format like this {"Historical Overview": "<Your Analysis Report>"}   """)},
                    {"role":"assistant","content": f"Here is Endpoint description: {endpoint_desc}, Here is JSON response: {response}"},
                    {"role": "user", "content": "I want you to perform a historical rank overview analysis for me by looking at the JSON file given to you."},
                    
                ]
            )
            result = json.loads(response.choices[0].message.content)
            return result
        else:
            return None

    
        

