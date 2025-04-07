# test_image_mining.py

from ai.miners.image_miner import mine_with_image

coin_name = "skycoin"
img_path = "assets/signs.jpg"  # Your test image path

mine_with_image(coin_name, img_path)
