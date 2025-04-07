# test_ai_mining.py

from ai.miners.text_miner import mine_with_text

coin_name = "skycoin"
sample_content = """
In the heart of the digital jungle, a lone dragon rose with pride.
Her wings cast sparks of hope, and her eyes glowed with resilience.
This is the age of Skycoin — fierce, fearless, free.
"""

mine_with_text(coin_name, sample_content)
