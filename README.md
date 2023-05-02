AI PARTY
AI Party is a tool for creating complex prompt chains quickly and easily. It is built using the GPT-3.5-turbo model.

Important Notes
The current version of AI Party is using the GPT-3.5-turbo model. To use another version of GPT or another LLM, you will need to rewrite the code slightly.

Usage
Download everything
Fill in the api_keys.txt file with one or multiple OpenAI API keys you want to use.
Simple Method
Use the AI Party Template to create your prompt chain.
Export your prompt chain as a CSV file.
Run ai_party_simple_run.py. The prompt chain file must be named "AIPartyChain.csv".
Profit :)
Code Method
Use the AI Party Template to create your prompt chain.
Export your prompt chain as a CSV file.
Import AI Party to your code using from ai_party import *.
Create a chain with chain = Chain(filepath). The filepath should lead to the CSV file exported from the AI Party Template.
Load blocks to your chain using chain.load_blocks().
Run the chain using chain.run().
Your final code should look like this:
