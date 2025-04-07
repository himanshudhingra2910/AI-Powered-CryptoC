import os
from blockchain.blockchain import Blockchain
from wallet.wallet import Wallet
from user.user_manager import load_user, register_user
from ai.miners.text_miner import TextMiner
from ai.miners.image_miner import mine_with_image
from blockchain.metadata_manager import get_leaderboard, get_exchange_rates
from market.marketplace import list_content, purchase_content, generate_share_message, load_listings, get_testimonials

def main():
    # Ensure required directories exist
    os.makedirs("chains", exist_ok=True)
    os.makedirs("metadata", exist_ok=True)
    os.makedirs("wallet", exist_ok=True)
    os.makedirs("data/users", exist_ok=True)
    os.makedirs("marketplace", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("shared", exist_ok=True)

    # User Login/Registration
    username = input("Enter your username: ").strip()
    user = load_user(username)
    if not user:
        choice = input(f"User '{username}' not found. Register? (y/n): ").strip().lower()
        if choice == "y":
            if register_user(username):
                print("✅ User registered!")
                user = {"username": username}
            else:
                print("❌ Registration failed.")
                return
        else:
            print("Exiting...")
            return

    # Initialize wallet and blockchain for the user's chosen coin
    wallet = Wallet(username)
    coin_name = input("Enter your cryptocurrency name (or an existing coin): ").strip().lower()
    wallet.create_currency(coin_name)
    
    # Load user's blockchain for the chosen coin (stored in chains/)
    blockchain = Blockchain.load_from_file(coin_name)
    
    # Display Leaderboard and Exchange Rates
    print("\n📊 Crypto Leaderboard:")
    leaderboard = get_leaderboard()
    for i, (coin, score) in enumerate(leaderboard.items(), 1):
        print(f"{i}. {coin} — Score: {score}")

    if leaderboard:
        base_coin = list(leaderboard.keys())[0]
        print(f"\n💱 Exchange Rates (Base: {base_coin})")
        rates = get_exchange_rates(base_coin)
        for coin, rate in rates.items():
            print(f"1 {base_coin} = {rate} {coin}")

    # Let the user choose an action
    print("\nSelect an action:")
    print("1. Mine Currency")
    print("2. List Content on Marketplace")
    print("3. Purchase Content from Marketplace (by Title)")
    print("4. View My Wallet")
    print("5. View Trade Testimonials")
    choice = input("Enter your choice (1-5): ").strip()

    if choice == "1":
        print("\nChoose mining method:")
        print("1. Text Mining")
        print("2. Image Mining")
        method = input("Enter choice (1 or 2): ").strip()
        if method == "1":
            text = input("Enter your creative text: ").strip()
            miner = TextMiner(blockchain, wallet)
            miner.mine_text(text, coin_name)
        elif method == "2":
            img_path = input("Enter path to your image (e.g., assets/yourimage.jpg): ").strip()
            mine_with_image(coin_name, img_path)
        else:
            print("Invalid mining choice.")
    elif choice == "2":
        title = input("Enter title for your content: ").strip()
        content = input("Enter your content (text or image URL): ").strip()
        content_type = input("Content type (poem/image/article): ").strip().lower()
        price = float(input("Set a price for your content: ").strip())
        # Here we assume the marketplace listing should be blocked if published is True.
        published_input = input("Is this content already published online? (y/n): ").strip().lower()
        published = True if published_input == "y" else False
        listing_id = list_content(username, title, content, price, coin_name, content_type, published)
        if listing_id:
            print(f"Listing created with ID: {listing_id}")
        else:
            print("Failed to list content. (It may be flagged as published.)")
    elif choice == "3":
        # Purchase content by title instead of listing ID.
        title_query = input("Enter the title of the content to purchase: ").strip().lower()
        listings = load_listings()
        matching_listings = [listing for listing in listings if title_query in listing.get("title", "").lower()]
        
        if not matching_listings:
            print("No listings found matching that title.")
        elif len(matching_listings) > 1:
            print("Multiple listings found. Please refine your search. Matches:")
            for listing in matching_listings:
                print(f"ID: {listing['id']} - Title: {listing['title']}")
        else:
            listing_id = matching_listings[0]["id"]
            result = purchase_content(username, listing_id)
            print(result)
            # After purchase, generate and display a shareable message
            share_msg = generate_share_message(username, matching_listings[0])
            print("Shareable Message:")
            print(share_msg)
    elif choice == "4":
        print("\n🧾 Your Wallet Balances:")
        for coin, amount in wallet.get_balances().items():
            print(f"  - {coin.capitalize()}: {amount}")
    elif choice == "5":
        testimonials = get_testimonials()
        if testimonials:
            print("\n📢 Trade Testimonials:")
            for testimonial in testimonials:
                print(f"  - {testimonial}")
        else:
            print("No testimonials yet.")
    else:
        print("Invalid choice!")

    # Save updated blockchain data for the coin
    blockchain.save_to_file(coin_name)
    
    # Display updated wallet balances at the end
    print("\n🔄 Updated Wallet Balances:")
    for coin, amount in wallet.get_balances().items():
        print(f"  - {coin.capitalize()}: {amount}")

if __name__ == "__main__":
    main()
