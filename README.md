# AI PARTY - Automate Everything And Anything
`ai_party` is a tool for creating complex prompt chains quickly and easily. It is built using the GPT-3.5-turbo model.

## Important Notes
The current version of AI Party is using the GPT-3.5-turbo model. To use another version of GPT or another LLM, you will need to rewrite the code slightly.

## Usage
>I will soon make it so you can do pip install. Never did it, so I need time to figure it out

### Instalation
1. Download everything
2. Fill in the api_keys.txt file with one or multiple OpenAI API keys you want to use.

## Simple Use (no code)
1. Use the [AI Party Template](https://docs.google.com/spreadsheets/d/1p5rieAyoTvVfPJvbFq8O2XNx27A3xvkii50k0n_gMXw/edit?usp=sharing) to create your prompt chain.
2. Export your prompt chain as a CSV file.
3. Run ai_party_simple_run.py. The prompt chain file must be named "AIPartyChain.csv".
4. Profit :)

## Code Method
1. Use the AI Party Template to create your prompt chain.
2. Export your prompt chain as a CSV file.
3. Import AI Party to your code using from 'ai_party import *' (or any other way).
4. Create chain (The filepath should lead to the CSV file exported from the AI Party Template.)
```python
chain = Chain(filepath).
```
  
  
5. Load blocks to your chain
```python
chain.load_blocks().
```
6. Run the chain
```python
chain.run().
```
Your final code should look like this:
```python
chain = Chain(r"G:\AI stuff\ScoringIdeaGenerator\AiParty\AiPartyTemplate.csv")
chain.load_blocks()
chain.run()
```



# AI Party Template
AI Party Template is a spreadsheet with specially prepared columns that allows you to easily fill every row with your values and export it as a CSV file to later use as list of instructions for AI Party.

You can use:
* [Google Sheets version](https://docs.google.com/spreadsheets/d/1p5rieAyoTvVfPJvbFq8O2XNx27A3xvkii50k0n_gMXw/edit?usp=sharing)
* File "AiPartyTemplate.xlsx"

## Types
The first column is named "Type".
It represents the type of action that the row will perform. 
Each type has a different function and uses a different number of columns to operate. 

The following types are currently available:
* Prompt -  sends message to AI
* Placeholder - creates placeholder
* (NOT YET WORKING) Code - run code from file(or just text in cell)
* (NOT EXIST YET) Chain - run another prompts chain from csv file

### Prompt
The Prompt type represents sending a regular message to gpt-3.5-turbo. It uses every column.

* ***Prompt type column***

  * **CONTINUE**: Continues the previous chat with AI. It's like sending the next message to ChatGPT.
  * **CONTINUE_ONE**: Same as CONTINUE, but neither this nor the AI's answer will be saved to the chat log. The AI will not remember this message or its reply. (It's like deleting the message and answer after sending one in Chat GPT)
  * **NEW**: Clears the chat story and sends this message to AI.
  * **ONE**: Just sends one message to AI in a new chat. It's like creating a new chat, sending a message there, receiving an answer, and closing the chat.
  
* ***Role Column: Sets the role of the message:***

  * **USER**: user message
  * **ASSISTANT**: assistant message
  * **SYSTEM**: system message
You can read more about roles on the OpenAI website.
* ***Content Column:***<br />
Message to send to AI. Placeholders will be automatically replaced. (Read about placeholders below)

* ***Placeholder name Column:*** <br />
If you put anything here, it will become the placeholder name and AI reply will become it's contents.

* ***File name Column:***<br />
If you put anything here, AI's reply will be saved to a file with the same name in the folder where ai_party.py is located.  <br />You should save txt files (e.g., "output.txt"). I don't know what will happen if you try saving files of different formats.

### Placeholder
The Placeholder type creates a placeholder that can be used later. It uses the "Content" and "Placeholder name" columns.

* ***Content Column:***<br />
Contents of Placeholder (What will be the placeholder replaced with).

* ***Placeholder name Column:***<br />
Name of the placeholder (What the placeholder will replace). I suggest using "{}" to avoid potential problems.

### Code
The Code type runs code in the content and executes it. However, it may not work correctly at the moment. I will update it to work stably later.

## How to use Placeholders
After creating a placeholder, any piece of text that equals the placeholder name will be replaced with the placeholder contents.<br />
For example:

>* Placeholder name: "{website_description}"
>* Placeholder content: "I need a very cool website for my Among Us server."
>* Message content: "Create a webpage based on an order: {website_description}"
>* What AI will receive: "Create a webpage based on an order: I need a very cool website for my Among Us server."


## Examples:
* [Website Design Generator](https://docs.google.com/spreadsheets/d/1jIZlorW3R_cAcllNgYoqyfQ4nSGCWscb0LnJTBMm0AA/edit?usp=sharing)
