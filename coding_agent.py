#LLMs The Brain:
from base_agent import BaseAgent
from google.genai import types

#The structured output:
from pydantic import BaseModel, field_validator, ConfigDict
from typing import List, Literal, Optional

#The tools:
import os
import json
import subprocess #For executing commands on the terminal

class CodeSchema(BaseModel):
    #Enable field validation from pydantic
    model_config = ConfigDict(validate_default=True)

    kind: Literal["code", "command"]
    filename: Optional[str] = None
    code: Optional[List[str]] = None
    command: Optional[str] = None

    #cls is the class, v is the value, info is the resulting schema
    @field_validator("code", mode="after")
    def code_required(cls, v, info):
        if info.data.get("kind") == "code" and not v:
            raise ValueError("[DEBUG] code[] required when kind='code'")
        return v

    @field_validator("command", mode="after")
    def command_required(cls, v, info):
        if info.data.get("kind") == "command" and not v:
            raise ValueError("[DEBUG] command required when kind='command'")
        return v

class ArrayOfCode(BaseModel):
    Output: List[CodeSchema]

class CodingAgent(BaseAgent):
    def __init__(self, model_name:str, system_prompt:str="", input:str=""):
        super().__init__(model_name, system_prompt)
        config = types.GenerateContentConfig(system_instruction=system_prompt,
        response_mime_type="application/json",
        response_schema=ArrayOfCode)

        self.gemini_output = self.call_LLM(input, config)
        print(self.gemini_output.text)
        print(self.gemini_output.parsed)

        with open("test2.txt", "w") as f:
            f.write(str(self.gemini_output.parsed))
        #with open("example.txt", "r") as f:
            #self.example_output_JSON = f.read()
        

    def run_subprocess():
        pass
    



if __name__ == "__main__":
    with open("system_prompt.txt", "r") as f:
        prompt = f.read()

    input = "Build a calculator app in python"

    agent = CodingAgent("gemini-2.5-flash", system_prompt=prompt, input=input)