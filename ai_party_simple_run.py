from ai_party import *


chain = Chain(r"G:\AI stuff\ScoringIdeaGenerator\AiParty\AiPartyTemplate.csv")
chain.load_blocks()
print(chain.blocks[0].content)
chain.run()

