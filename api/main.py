from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from pydantic import BaseModel
from typing import Dict, Any, List
import os, json
from datetime import datetime

# Import your backend modules – adjust the paths as needed.
from wallet.wallet import Wallet
from blockchain.blockchain import Blockchain
from blockchain.metadata_manager import get_leaderboard, get_exchange_rates
from ai.miners.text_miner import TextMiner
from ai.miners.image_miner import mine_with_image
from market.marketplace import (
    list_content, 
    purchase_content, 
    search_listings,
    generate_share_message,
    load_listings,
    get_testimonials
)

app = FastAPI(title="AI-Powered Blockchain Crypto API", version="1.0")

# -------------------------------
# Pydantic Models for API Inputs
# -------------------------------

class TradeRequest(BaseModel):
    from_currency: str
    to_currency: str
    amount: float

class MineTextRequest(BaseModel):
    coin_name: str
    text: str

class ListContentRequest(BaseModel):
    creator: str
    title: str
    content: str
    price: float
    currency: str
    content_type: str
    published: bool = False

class ShareRequest(BaseModel):
    buyer: str
    listing_id: str

class PurchaseContentRequest(BaseModel):
    buyer: str
    listing_id: str

class ShareMomentRequest(BaseModel):
    user: str
    content: str
    reward: float
    currency: str
    content_type: str

# -------------------------------
# API Endpoints
# -------------------------------

# Wallet Endpoints
@app.get("/wallet/{username}", response_model=Dict[str, Any])
def get_wallet(username: str):
    wallet = Wallet(username)
    return {"wallet": wallet.get_balances()}

@app.post("/wallet/{username}/trade", response_model=Dict[str, Any])
def trade_wallet(username: str, trade: TradeRequest):
    wallet = Wallet(username)
    # Use the 'from_currency' as the base for exchange rate calculation
    exchange_rates = get_exchange_rates(trade.from_currency.lower())
    success = wallet.trade_currency(trade.from_currency, trade.to_currency, trade.amount, exchange_rates)
    if not success:
        raise HTTPException(status_code=400, detail="Trade failed")
    return {"wallet": wallet.get_balances()}

# Mining Endpoints
@app.post("/mine/text", response_model=Dict[str, Any])
def mine_text(request: MineTextRequest):
    # For this demo, we use a dummy username; in a real app, use proper authentication.
    username = "dummy_user"
    wallet = Wallet(username)
    blockchain = Blockchain.load_from_file(request.coin_name.lower())
    miner = TextMiner(blockchain, wallet)
    miner.mine_text(request.text, request.coin_name.lower())
    return {"wallet": wallet.get_balances()}

@app.post("/mine/image", response_model=Dict[str, Any])
def mine_image(coin_name: str, file: UploadFile = File(...)):
    # Save the uploaded image temporarily.
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(file.file.read())
    # Perform image mining.
    mine_with_image(coin_name.lower(), temp_path)
    os.remove(temp_path)
    # For this demo, we use a dummy username.
    wallet = Wallet("dummy_user")
    return {"wallet": wallet.get_balances()}

# Leaderboard Endpoint
@app.get("/leaderboard", response_model=Dict[str, Any])
def leaderboard():
    lb = get_leaderboard()
    return {"leaderboard": lb}

# Marketplace Endpoints
@app.post("/marketplace/list", response_model=dict)
def list_marketplace_item(request: ListContentRequest):
    listing_id = list_content(
        request.creator, request.title, request.content, 
        request.price, request.currency, request.content_type, 
        published=request.published
    )
    if listing_id is None:
        raise HTTPException(status_code=400, detail="Content is published and cannot be listed.")
    return {"listing_id": listing_id}

@app.get("/marketplace/search", response_model=Dict[str, Any])
def search_marketplace(q: str = Query(..., description="Search query for content titles")):
    """
    Search marketplace listings by content title.
    """
    results = search_listings(q)
    if not results:
        raise HTTPException(status_code=404, detail="No listings found matching your query.")
    return {"results": results}

@app.post("/marketplace/buy", response_model=Dict[str, Any])
def buy_marketplace_item(request: PurchaseContentRequest):
    result = purchase_content(request.buyer, request.listing_id)
    if "Insufficient" in result or "not found" in result:
        raise HTTPException(status_code=400, detail=result)
    
    # After a successful purchase, generate the share message.
    listings = load_listings()
    listing = next((l for l in listings if l["id"] == request.listing_id), None)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found for sharing.")
    share_msg = generate_share_message(request.buyer, listing)
    return {"message": result, "share_message": share_msg}

# Sharing "Treasure Moment" Endpoint
@app.post("/share/moment", response_model=Dict[str, Any])
def share_moment(request: ShareMomentRequest):
    share_dir = "shared"
    os.makedirs(share_dir, exist_ok=True)
    share_file = os.path.join(share_dir, f"{request.user}_shared.json")
    shared_data = {
        "user": request.user,
        "shared_type": request.content_type,
        "content": request.content,
        "reward": request.reward,
        "currency": request.currency.lower(),
        "timestamp": datetime.utcnow().isoformat()
    }
    with open(share_file, "w") as f:
        json.dump(shared_data, f, indent=4)
    return {"message": f"{request.user}'s moment shared successfully!"}

@app.get("/shared/{user}", response_model=Dict[str, Any])
def get_shared_moment(user: str):
    share_file = os.path.join("shared", f"{user}_shared.json")
    if not os.path.exists(share_file):
        raise HTTPException(status_code=404, detail="No shared moment found for this user.")
    with open(share_file, "r") as f:
        shared_data = json.load(f)
    return {"shared_moment": shared_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
