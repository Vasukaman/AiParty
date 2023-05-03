from ai_party import *
import os


filename = "AiPartyTemplate.csv"
filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), filename))
chain = Chain(filepath)
chain.load_blocks()
print(chain.blocks[0].content)
chain.run()

