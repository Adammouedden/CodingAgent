#LLMs The Brain:
import ollama
from google import genai
from openai import OpenAI
from xai_sdk import Client

#The structured output:
from pydantic import BaseModel

#The tools:
import os
import subprocess #For executing commands on the terminal

class Code(BaseModel):
    instruction_type: str #Execute, create, debug, open, etc
    instructions: list[str] #Command line input, code, etc
    
class CodingAgent:
    def __init__(self, model_name:str, api_key:str="",):
        self.model_name = model_name
        if ("gemini" in model_name):
            
            google_models = self.client.models.list_language_models()
            if model_name not in google_models:
                print(f"{model_name} is not a Google model")
                return
            
            self.client = genai.Client(api_key=api_key)
            self.key = "Google"
            
        if ("gpt" in model_name):
            self.client = OpenAI(api_key=api_key)
            self.key = "OpenAI"
            
        if ("grok" in model_name):
            self.client = Client(api_key=api_key)
            self.key = "Grok"
            
        else:
            print(f"{model_name} is not yet supported")
            
    def prompt_agent(self, input:list, system_prompt:str=""):
        match self.key:
            case "Google":
                
                self.response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=system_prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_schema": list[Code]
                    }
                )
                
                return self.response
            
            case "OpenAI":
                pass
            
            case "Grok":
                pass
            
    def execute_code(self, response):
        pass
                
                
                