#This is main file of ai_party
#I tried writing explanation comments and keeping consistant style
#But this is like my first python project(I only coded games in unity before), so don't kill me if it's not the best, pls:)
#ඞ

from asyncio.windows_events import NULL
from typing import List, Union
from enum import Enum
import subprocess
from email import message
import openAI
import sys

from utils import *
from json import load




#Enum for block types
class ChainType(Enum):
    PROMPT = 1
    CODE = 2
    PLACEHOLDER = 3
#Enum for promt types
class PromptType(Enum):
    NEW = 1
    CONTINUE = 2
    CONTINUE_ONE = 3
    ONE = 4
#Enum for role types
class Role(Enum):
    USER = 1
    ASSISTENT = 2
    SYSTEM = 3

#GENERAL CHAIN BLOCK CLASS
#---------------------------------------------------------------------------------------------------------------#

#General part of executable chain. 
#Any block and chain itself is a chain block.
#Chain block then added to chain
class ChainBlock:


    #content is prompt, code or placeholder
    #result is a result of run of this block. PromptBlock will output OpenAI answer. Code will output result of the code. Placeholder has no result.
    #result_placeholder_name is a name of placeholder(ex {placeholder}).  Result of the block will be put into this {result_placeholder_name}
    #result_filename is a name of a file(ex file.txt). Result of the block will be put into this file.txt
    #placeholder_replacements is a list of already existing placeholders
    def __init__(self, content:str, result_placeholder_name:str, result_filename:str):
         self.content = content 
         self.result = ""
         self.result_placeholder_name = result_placeholder_name
         self.result_filename = result_filename      
         self.placeholder_replacements = {}

    #method that saves result to result_filename 
    def save_result_to_txt_file(self):
       if self.result_filename and self.result_filename!="-":
           path = get_folder_path(__file__)
           path+=f"\\{self.result_filename}"
           save_txt_file(path,self.result)

    #general run method
    def run(self, messages:List[str], current_chain:"Chain", openAi_object:openAI.OpenAI) -> str:
        self.result = ""
        return self.result

    #method that adds or replaces {placelader_name} in current ChainBlock.
    #It only makes sense to update placeholders in chain
    def add_placeholder_replacement(self, placeholder_name, placehodler_replacement):
         if (placeholder_name!=""):
             self.placeholder_replacements.update({placeholder_name:placehodler_replacement})

    #method to replace all palceholders(from placeholder_replacements) in content
    def replace_placeholders(self):
        placeholders = get_placeholders(self.content)
        for placehodler in placeholders:
            if placehodler in self.placeholder_replacements:
                self.content = replace_placeholder(self.content,placehodler, self.placeholder_replacements[placehodler])


#PLACEHOLDER CHAIN BLOCK CLASS
#---------------------------------------------------------------------------------------------------------------#
#block that just adds placeholder to the chain.
class PlaceholderBlock(ChainBlock):
     def __init__(self,placeholder_name:str ,content:str):
         self.placeholder_name = placeholder_name
         self.content = content


     def run(self,messages:List[str], current_chain:"Chain", openAi_object:openAI.OpenAI):
         current_chain.add_placeholder_replacement(self.placeholder_name,self.content)
         





#CODE CHAIN BLOCK CLASS. 
#---------------------------------------------------------------------------------------------------------------#
#block that runs code and places output into result
#IM NOT SURE IF IT"S WORK SOSOSOSO SORRY
#I'M GONNA TEST, FIX AND MAKE IT WORK SOON
#SORRY
#ඞ
#a u
class CodeBlock(ChainBlock):
     def __init__(self, content:str, result_placeholder_name:str, result_filename:str):
         self.content = content
         self.result = ""
         self.result_placeholder_name=result_placeholder_name
         self.result_filename=result_filename


     def run(self, messages:List[str], current_chain:"Chain", openAi_object:openAI.OpenAI) -> str:

         self.replace_placeholders()

         # Run the code in a subprocess and capture its output.
         # I'll be honest. ChatGPT wrote this part. I have no idea if this is a good way to do this:)
         result = subprocess.check_output(["python", "-c", self.content], universal_newlines=True)
         self.result = result.strip()

         current_chain.add_placeholder_replacement(self.result_placeholder_name,self.result)
         self.save_result_to_txt_file()
         return self.result






#MESSAGE TO AI CHAIN BLOCK CLASS
#---------------------------------------------------------------------------------------------------------------#
class AIMessageBlock(ChainBlock):

    #prompt_type is NEW/CONTINUE/CONTINUE_ONE/ONE. This is bc I use chat version of GPT (gpt-3.5-turbo), which allows to send messages in a chat style. More explanaition of each type in documentation
    #role is User/Assistant/System. Also bc of chat version of GPT. This is a role of a message. https://platform.openai.com/docs/guides/chat
    #content is prompt, code or placeholder
    #result is a result of run of this block. PromptBlock will output OpenAI answer. Code will output result of the code. Placeholder has no result.
    #result_placeholder_name is a name of placeholder(ex {placeholder}).  Result of the block will be put into this {result_placeholder_name}
    #result_filename is a name of a file(ex file.txt). Result of the block will be put into this file.txt
    #placeholder_replacements is a list of already existing placeholders
    def __init__(self, prompt_type:str, role:str, content:str, result_placeholder_name:str, result_filename):
        self.prompt_type = check_enum_and_return_name(prompt_type,PromptType)
        self.role = check_enum_and_return_name(role, Role)
        self.content = content
        self.result = ""
        self.result_placeholder_name=result_placeholder_name
        self.result_filename=result_filename
        self.placeholder_replacements = {}

            

    #This method sends message to OpenAI gpt-3.5-turbo and puts it's answer in result, placehodler(if name given) and file(if name given)
    def run(self, messages:List[str], current_chain:"Chain", openAi_object:openAI.OpenAI) -> List[str]:

        #replace placeholders in content
        self.replace_placeholders()

        #print message to console
        print(f"\n{self.prompt_type.name} MESSAGE:" + self.content)

        #Prompt Type = CONTINUE
        if self.prompt_type == PromptType.CONTINUE:
            messages.append(openAI.OpenAiChatMessage(self.role.name.lower(), self.content))   
            self.result = openAi_object.generate_openAI_response(messages)
            messages.append(openAI.OpenAiChatMessage(self.role.name.lower(),self.result))

        #Prompt Type = CONTINUE_ONE
        elif self.prompt_type == PromptType.CONTINUE_ONE:
            temp_messages = messages

            temp_messages.append(openAI.OpenAiChatMessage(self.role.name.lower(), self.content))
            self.result = openAi_object.generate_openAI_response(temp_messages)

        #Prompt Type = NEW
        elif self.prompt_type == PromptType.NEW:
            messages = [openAI.OpenAiChatMessage(self.role.name.lower(), self.content)]
            self.result = openAi_object.generate_openAI_response(messages)
            messages.append(openAI.OpenAiChatMessage(self.role.name.lower(),self.content))

        #Prompt Type = ONE
        elif self.prompt_type == PromptType.ONE:

            temp_messages = [openAI.OpenAiChatMessage(self.role.name.lower(), self.content)]
            self.result = openAi_object.generate_openAI_response(temp_messages)

        #Promt Type is incorrect
        else:
            print("prompt_type is not correct") 

        #print reply to console
        print(f"\nREPLY:"+self.result)

        #add/replace placeholder
        current_chain.add_placeholder_replacement(self.result_placeholder_name,self.result)

        #save result to file
        self.save_result_to_txt_file()

        return messages


   
        
   
#CHAIN CLASS
#---------------------------------------------------------------------------------------------------------------#    

#filepath is a path to CSV file with chain
#messages is a list of chat messages with AI
#blocks is a list of blocks(like AIMessageBlock, PlaceholderBlock)
class Chain(ChainBlock):
     def __init__(self, filepath:str):
         self.filepath = filepath
         self.messages = List[str]
         self.blocks = []
         self.result = None
         self.placeholder_replacements = {}
         self.output_filepath = "" #not used yet
         self.openAi_object = openAI.OpenAI()
       

     #This method goes throught all blocks one by one and runs each of them
     def run(self) -> str:
         for i,block in enumerate(self.blocks):
            #Check if block is AIMessage block
            if isinstance(block, AIMessageBlock):
                #adds placeholders to block. Probably not the best way to work with placeholders. But for now it's ok.
                block.placeholder_replacements=self.placeholder_replacements

                #If it's not the first block in the chain, then add placeholder {last_result} to it.
                if (i > 0) and (hasattr(self.blocks[i-1], "result")):
                    block.add_placeholder_replacement("last_result",self.blocks[i-1].result)

            #Add result of a AIMessageBlock to ai chat messages. (if it is promt_type=ONE/CONTINUE_ONE it will just return the old messages without new one)
            self.messages = block.run(self.messages, self, self.openAi_object)
          
         #return result of a last block   
         return self.blocks[-1].result

     #This method loads blocks from CSV file into self.blocks
     def load_blocks(self):

         dict_list = csv_to_dict_list(self.filepath)

         for future_block in dict_list:
            if future_block["Type"] == "Prompt":
                block = AIMessageBlock(future_block["Promt Type"],future_block["Role"],future_block["Content"], future_block["Placeholder Name"], future_block["File Name"])
                self.blocks.append(block)
            elif future_block["Type"] == "Code":
                block = CodeBlock(future_block["Content"])
                self.blocks.append(block)
            elif future_block["Type"] == "Placeholder":
                block = PlaceholderBlock(future_block["Placeholder Name"],future_block["Content"])
                self.blocks.append(block)
                

 
          
