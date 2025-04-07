import os
import json
import uuid
import logging
from datetime import datetime
from wallet.wallet import Wallet

# Configure a logger
logger = logging.getLogger("MarketplaceLogger")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.FileHandler("logs/marketplace.log")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

MARKETPLACE_FILE = "marketplace/listings.json"

def load_listings():
    if not os.path.exists(MARKETPLACE_FILE):
        return []
    with open(MARKETPLACE_FILE, "r") as f:
        return json.load(f)

def save_listings(listings):
    with open(MARKETPLACE_FILE, "w") as f:
        json.dump(listings, f, indent=4)

def list_content(creator, title, content, price, currency, content_type, published=False):
    """
    List content on the marketplace.
    
    :param creator: Username of the content creator.
    :param title: Title of the content.
    :param content: The content itself (text or image URL).
    :param price: Price for the content.
    :param currency: Currency in which the price is denominated.
    :param content_type: Type of content (e.g., "poem", "image", "article").
    :param published: Boolean flag; if True, the content is already published online.
    :return: Listing ID if successful; otherwise, None.
    """
    if published:
        print("🚫 This content is already published online and cannot be listed in the marketplace.")
        return None

    listings = load_listings()
    listing = {
        "id": f"{creator}_{uuid.uuid4().hex[:6]}",
        "creator": creator,
        "title": title,
        "content": content,
        "content_type": content_type,
        "price": price,
        "currency": currency.lower(),
        "buyers": []
    }
    listings.append(listing)
    save_listings(listings)
    print(f"📢 Content '{title}' listed successfully by {creator}.")
    return listing["id"]

def purchase_content(buyer, listing_id):
    listings_file = "marketplace/listings.json"
    with open(listings_file, "r") as f:
        listings = json.load(f)

    for listing in listings:
        if listing["id"] == listing_id:
            price = listing["price"]
            currency = listing["currency"].lower()
            creator = listing["creator"]

            # Load buyer's and seller's wallets using the Wallet class.
            # (Assuming you have functions to load/update wallets)
            buyer_wallet = Wallet(buyer)
            seller_wallet = Wallet(creator)

            # Check buyer's balance
            if buyer_wallet.get_balances().get(currency, 0) < price:
                logger.warning(f"Purchase failed: {buyer} has insufficient funds for {listing_id}.")
                return "Insufficient funds"

            # Deduct from buyer
            buyer_wallet.data["currencies"][currency] -= price
            buyer_wallet.save_wallet()

            # Credit seller
            seller_wallet.credit(currency, price)

            # Record buyer in listing
            listing["buyers"].append({
                "buyer": buyer,
                "amount": price,
                "timestamp": datetime.utcnow().isoformat()
            })

            # Save updated listings
            with open(listings_file, "w") as f:
                json.dump(listings, f, indent=4)

            # Log the trade details
            logger.info(f"Trade executed: Buyer {buyer} purchased '{listing['title']}' from {creator} for {price} {currency} (Listing ID: {listing_id}).")
            return f"{buyer} bought '{listing['title']}' from {creator} for {price} {currency}"
    
    logger.error(f"Purchase failed: Listing {listing_id} not found.")
    return "Listing not found"

def generate_share_message(buyer, listing):
    """
    Generates a shareable message when a buyer purchases content.
    
    :param buyer: The username of the buyer.
    :param listing: The listing dictionary with content details.
    :return: A shareable string.
    """
    platform_name = "AI-Powered Crypto Platform"  # Update with your platform name if desired.
    title = listing.get("title", "Untitled")
    creator = listing.get("creator", "Unknown")
    price = listing.get("price", 0)
    currency = listing.get("currency", "crypto").upper()

    message = (
        f"I just bought '{title}' by {creator} for {price} {currency} on {platform_name}! "
        "Join me and experience the future of creative crypto!"
    )
    return message

def get_testimonials():
    """
    Returns a list of testimonial strings for all trades.
    """
    listings = load_listings()
    feed = []
    for listing in listings:
        for buyer in listing.get("buyers", []):
            feed.append(
                f"🪙 {buyer['buyer']} bought '{listing['title']}' from {listing['creator']} for {buyer['amount']} {listing['currency']}"
            )
    return feed

def search_listings(query: str):
    """
    Search marketplace listings by title.

    :param query: A search string.
    :return: A list of listings whose titles contain the query (case-insensitive).
    """
    listings = load_listings()
    # Filter listings where the query appears in the title (case-insensitive)
    filtered = [
        listing for listing in listings
        if query.lower() in listing.get("title", "").lower()
    ]
    return filtered

