import requests
from typing import List
import time
class OpenAiChatMessage:
    def __init__(self, role:str, message:str) -> None:
        self.role = role
        self.message = message

def load_api_keys(filepath:str) -> List[str]:
    with open(filepath, 'r') as f:
        api_keys = f.readlines()
        api_keys = [key.strip() for key in api_keys]
    return api_keys


class OpenAI:
    def __init__(self) -> None:
        self.api_index = 0
        self.api_keys = load_api_keys(r"G:\AI stuff\ScoringIdeaGenerator\AiParty\api_keys.txt")

    def generate_openAI_response(self,messages:List[OpenAiChatMessage]) -> str:
        
        done = False
        while(not done):
            next_index = (self.api_index + 1) % len(self.api_keys)  # calculate the next index
            # this will be 4, which is the next index after 3 in this array

            self.api_index = next_index  # move to the next index
          
   
          
            # Replace YOUR_API_KEY with your actual OpenAI API key
            headers = {"Authorization": "Bearer "+self.api_keys[self.api_index]}
            url = "https://api.openai.com/v1/chat/completions"

            # Convert the list of messages to a list of dictionaries
            message_list = [{"role": message.role, "content": message.message} for message in messages]

            data = {
                "model": "gpt-3.5-turbo",
                "messages": message_list,    
                "temperature": 0.35
            }

            response = requests.post(url, headers=headers, json=data)
            response_json = response.json()

        

            if response.status_code == 200:
                answer = response_json["choices"][0]["message"]['content']
                #print(f"ChatGPT: {answer}")
                return answer
                done=True
            else:
                pass
            #    print("Error: Failed to receive response from OpenAI's API")
             #   print("Waiting...")
               # print(response_json)

            time.sleep(5)



