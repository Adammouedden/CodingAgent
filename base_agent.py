#LLMs The Brain:
import ollama
from google import genai
from google.genai import types
from openai import OpenAI
from xai_sdk import Client

from dotenv import load_dotenv
import os

load_dotenv()

class BaseAgent():
    def __init__(self, model_name: str, system_prompt:str=""):
        self.model_name = model_name
        self.config = None

        match model_name:

            case model_name if "gemini" in model_name:
                api_key = os.getenv("GOOGLE_API")
                self.client = genai.Client(api_key=api_key)
                self.chat_function = self.client.models.generate_content #Python magic, pass the function into a variable/object
                self.config = types.GenerateContentConfig(
                    system_instruction=system_prompt
                )
                

            case model_name if "gpt" in model_name:
                api_key = os.getenv("OPENAI_API")
                self.client = OpenAI()
                self.chat_function = self.client.responses.create

            case model_name if "grok" in model_name:
                print("XAI model")

            case _:
                print("This model is not yet supported.")


    def call_LLM(self, input, config=None):
        custom_configuration = None
        if config != None:
            custom_configuration = config #Custom Configuration passed in to this function from the user
        else:
            custom_configuration = self.config #Default Base Agent Configuration

        output = self.chat_function(model=self.model_name, contents=input, config=custom_configuration)
        return output
        





if __name__ == "__main__":
    #system_instruction = ""
    #config = types.GenerateContentConfig(system_instruction=system_instruction, tools=[types.Tool(code_execution=types.ToolCodeExecution)])
    #agent = BaseAgent("gemini-2.5-flash")
    #agent.call_LLM("Solve fibonnaci where n = 20", config=config)
    pass
    