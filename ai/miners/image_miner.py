# image_miner.py

from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
from blockchain.blockchain import Blockchain
from blockchain.metadata_manager import MetadataManager

# Load model & processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Predefined aesthetics
concepts = ["artistic", "vibrant", "futuristic", "surreal", "sci-fi"]

def score_image(img_path):
    image = Image.open(img_path).convert("RGB")
    inputs = processor(text=concepts, images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)

    score = torch.max(probs).item()
    matched_concept = concepts[torch.argmax(probs)]
    
    return score, matched_concept

def mine_with_image(coin_name, img_path):
    print(f"\n🖼️ Mining with image for {coin_name}...")

    score, concept = score_image(img_path)
    print(f"🎨 Matched concept: {concept}, Score: {score:.2f}")

    # Define reward thresholds
    if score > 0.75:
        reward = 40
    elif score > 0.5:
        reward = 25
    else:
        reward = 10

    # Load blockchain
    chain = Blockchain.load_from_file(coin_name)
    chain.add_transaction(f"Image uploaded with concept '{concept}' - score: {score:.2f}")
    chain.mine_pending_transactions()
    chain.save_to_file(coin_name)

    # Update metadata
    meta = MetadataManager.load_metadata(coin_name)
    meta["uploads"] += 1
    meta["mines"] += 1
    meta["score"] += reward
    MetadataManager.save_metadata(coin_name, meta)

    print(f"✅ {coin_name} mined with +{reward} points!\n")
