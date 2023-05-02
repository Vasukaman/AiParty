from asyncio.windows_events import NULL
from typing import List, Union
from enum import Enum
import subprocess
from email import message
import openAI
import sys

from utils import *
from json import load



class ChainType(Enum):
    PROMPT = 1
    CODE = 2
    PLACEHODLER = 3

class PromtType(Enum):
    NEW = 1
    CONTINUE = 2
    CONTINUE_ONE = 3
    ONE = 4

class Role(Enum):
    USER = 1
    ASSISTENT = 2
    SYSTEM = 3


#General part of executable chain. 
class ChainBlock:
    def __init__(self, content:str, result_placeholder_name:str, result_filename:str):
         self.content = content
         self.result_placeholder_name
         self.result_filename = result_filename
         self.result = ""
         self.placeholder_replacements = {}


    def save_result_to_txt_file(self):
       if self.result_filename and self.result_filename!="-":
           path = get_folder_path(__file__)
           path+=f"\\{self.result_filename}"
           save_txt_file(path,self.result)

    def run(self, current_chain:"Chain") -> str:
        self.result = ""
        return self.result

    def add_placeholder_replacement(self, placeholder_name, placehodler_replacement):
        self.placeholder_replacements.update({placeholder_name:placehodler_replacement})




class PlaceholderBlock(ChainBlock):
     def __init__(self,placeholder_name:str ,content:str):
         self.placeholder_name = placeholder_name
         self.content = content


     def run(self,messages:List[str], current_chain:"Chain", openAi_object:openAI.OpenAI):
        if (self.placeholder_name!=""):
            current_chain.add_placeholder_replacement(self.placeholder_name,self.content)
         



class CodeBlock(ChainBlock):
     def __init__(self, content:str):
         self.content = content
         self.result = ""


     def run(self) -> str:

         self.replace_placeholders()

         # Run the code in a subprocess and capture its output.
         # I'll be honest. ChatGPT wrote this part. I have no idea if this is a good way to do this:)
         result = subprocess.check_output(["python", "-c", self.code], universal_newlines=True)
         self.result = result.strip()
         return self.result



class AIMessageBlock(ChainBlock):
    def __init__(self, prompt_type:str, role:str, content:str, result_placeholder_name:str, result_filename):
        self.prompt_type = check_enum_and_return_name(prompt_type,PromtType)
        self.role = check_enum_and_return_name(role, Role)
        self.content = content
        self.result = ""
        self.placeholder_replacements = {}
        self.result_placeholder_name=result_placeholder_name
        self.result_filename=result_filename
    

    def replace_placeholders(self):
        placeholders = get_placeholders(self.content)
        for placehodler in placeholders:
            if placehodler in self.placeholder_replacements:
                self.content = replace_placeholder(self.content,placehodler, self.placeholder_replacements[placehodler])
            

    #ඞ
    def run(self, messages:List[str], current_chain:"Chain", openAi_object:openAI.OpenAI) -> List[str]:

        self.replace_placeholders()

        print(f"\n{self.prompt_type.name} MESSAGE:" + self.content)

        if self.prompt_type == PromtType.CONTINUE:
            messages.append(openAI.OpenAiChatMessage(self.role.name.lower(), self.content))   
            self.result = openAi_object.generate_openAI_response(messages)
            messages.append(openAI.OpenAiChatMessage(self.role.name.lower(),self.result))

        elif self.prompt_type == PromtType.CONTINUE_ONE:
            messages.append(openAI.OpenAiChatMessage(self.role.name.lower(), self.content))
            self.result = openAi_object.generate_openAI_response(messages)

        elif self.prompt_type == PromtType.NEW:
            messages = [openAI.OpenAiChatMessage(self.role.name.lower(), self.content)]
            self.result = openAi_object.generate_openAI_response(messages)
            messages.append(openAI.OpenAiChatMessage(self.role.name.lower(),self.content))

        elif self.prompt_type == PromtType.ONE:

            temp_messages = [openAI.OpenAiChatMessage(self.role.name.lower(), self.content)]
            self.result = openAi_object.generate_openAI_response(temp_messages)

        else:
            print("prompt_type is not correct") 

        print(f"\nREPLY:"+self.result)

        if (self.result_placeholder_name!=""):
            current_chain.add_placeholder_replacement(self.result_placeholder_name,self.result)

        self.save_result_to_txt_file()

        return messages


   
        
   
    

class Chain(ChainBlock):
     def __init__(self, filepath:str):
         self.filepath = filepath
         self.messages = List[str]
         self.blocks = []
         self.result = None
         self.placeholder_replacements = {}
         self.output_filepath = ""
         self.openAi_object = openAI.OpenAI()
       

     def run(self) -> str:
         for i,block in enumerate(self.blocks):
            if isinstance(block, AIMessageBlock):
                block.placeholder_replacements=self.placeholder_replacements
                if (i > 0) and (hasattr(self.blocks[i-1], "result")):
                    block.add_placeholder_replacement("lastResult",self.blocks[i-1].result)
                block.replace_placeholders()

            self.messages = block.run(self.messages, self, self.openAi_object)
            
         return self.blocks[-1].result

     def load_blocks(self):
         dict_list = csv_to_dict_list(self.filepath)
         for future_block in dict_list:
            if future_block["Type"] == "Prompt":
                block = AIMessageBlock(future_block["Promt Type"],future_block["Role"],future_block["Content"], future_block["Placeholder Name"], future_block["File Name"])
                self.blocks.append(block)
            elif future_block["Type"] == "Code":
                block = CodeBlock(future_block["Content"])
            elif future_block["Type"] == "Placeholder":
                block = PlaceholderBlock(future_block["Placeholder Name"],future_block["Content"])
                self.blocks.append(block)
                

 
          
