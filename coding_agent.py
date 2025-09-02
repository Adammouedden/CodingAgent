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
from pathlib import Path

#Debugging flags

writing_code = False
pydantic_test = False

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

class ArrayOfCode(BaseModel): #This will result in the LLM returning a dictionary
    commands: List[CodeSchema]

class CodingAgent(BaseAgent):
    def __init__(self, model_name:str, system_prompt:str=""):
        super().__init__(model_name, system_prompt)

        self.config = types.GenerateContentConfig(system_instruction=system_prompt,
                                                    response_mime_type="application/json",
                                                    response_schema=ArrayOfCode)

    def write_code(self, input:str=""):
        self.gemini_output = self.call_LLM(input, self.config)
        #print(self.gemini_output.text)
        #print(self.gemini_output.parsed)

        #For validation or you could just use self.gemini_output.parsed directly for a naive trusting approach
        if (pydantic_test):
            commands = [CodeSchema.model_validate(item) for item in self.gemini_output.parsed]
        else:
            commands = self.gemini_output.parsed

        payload = [commands.model_dump() for c in commands]
        
        #Dumps the pydantic model data into JSON
        with open("code_example1.txt", "w") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        
        
    def load_code(self):
        #Testing
        #Read saved code from the cache to reduce API useage during testing
        with open("code_example1.txt", "r") as f:
            commands_cached = f.read()
        

        cached_dict = json.loads(commands_cached) #Convert string to dictionary

        if (pydantic_test):
            commands = [CodeSchema.model_validate(item) for item in cached_dict] #Now validate it
        else:   
            commands = cached_dict

        output = self.execute(commands)
        print(output)


    def execute(self, commands):
        data = commands[0]["commands"]
        output = []
       
        for command in data:
           
            match command['kind']:
                case "code":
                    with open(command["filename"], "w") as f: 
                        text = "\n".join(command["code"])
                        f.write(text)

                case "command":
                    result = subprocess.run(["cmd", "/c", command["command"]], capture_output=True, text=True)

                    if result.returncode != 0:
                        print(f"An error has occured while executing: {result.stderr}")
                        raise ValueError("[DEBUG] Command error")

                    output.append(result.stdout)
            
        return output


if __name__ == "__main__":
    with open("system_prompt.txt", "r") as f:
        prompt = f.read()

    input = "Build the popular game Wordle on a React web app"

    agent = CodingAgent("gemini-2.5-flash", system_prompt=prompt)

    if (writing_code):
        agent.write_code(input)

    agent.load_code()