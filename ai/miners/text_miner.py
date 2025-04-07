from transformers import pipeline
from blockchain.blockchain import Blockchain
from blockchain.metadata_manager import MetadataManager
from ai.miners.utils.ai_detector import AIGeneratedTextDetector
from ai.miners.utils.search_detector import is_published_text


class TextMiner:
    def __init__(self, blockchain, wallet):
        self.blockchain = blockchain
        self.wallet = wallet
        self.analyzer = pipeline("sentiment-analysis")
        self.detector = AIGeneratedTextDetector()

    def calculate_adaptive_reward(self, score, length, published, user_uploads):
        """
        Adjust reward based on:
        - sentiment score (0.0 to 1.0)
        - length of the text
        - if it's published
        - user upload count
        """
        if published:
            return 5  # Hard cap for published content

        base = score * 100

        # Bonus or penalty based on length
        if length > 200:
            base += 10
        elif length < 50:
            base -= 10

        # Bonus for experienced users
        if user_uploads > 10:
            base += 5

        return max(5, int(base))  # Ensure reward isn't below 5

    def mine_text(self, text, coin_name):
        print("🧠 Checking if content is AI-generated...")

        is_ai, confidence = self.detector.is_ai_generated(text)
        if is_ai:
            print(f"⚠️ Detected as AI-generated content (Confidence: {confidence:.2f})")
            print("⛏️ Nothing found in this mine.")
            return False

        print("✅ Human-generated text confirmed.")

        print("🔍 Checking if content is already published online...")
        published, source_url = is_published_text(text)

        if published:
            print("⚠️ This text is already published online.")
            print(f"🔗 Source: {source_url}")
        else:
            print("✅ Original content detected.")

        # Get metadata early to read user history
        meta = MetadataManager.load_metadata(coin_name)
        user_uploads = meta.get("uploads", 0)

        # Analyze sentiment if original
        if not published:
            result = self.analyzer(text)[0]
            label = result["label"]
            score = round(result["score"], 2)
            self.blockchain.add_transaction(f"Sentiment: {label}, Confidence: {score}")
        else:
            score = 0.0  # Neutral for published content

        # Adaptive reward
        length = len(text.split())
        reward = self.calculate_adaptive_reward(score, length, published, user_uploads)

        # Block data
        self.blockchain.add_transaction(f"Text mined: {text}")
        if published:
            self.blockchain.add_transaction("⚠️ Published content used – limited reward")
        self.blockchain.add_transaction(f"Reward: {reward} {coin_name}")
        self.blockchain.mine_pending_transactions()

        # Update wallet
        self.wallet.credit(coin_name, reward)

        # Update metadata
        meta["uploads"] += 1
        meta["mines"] += 1
        meta["score"] += reward
        meta["published"] = published  # Flag it for marketplace use
        MetadataManager.save_metadata(coin_name, meta)

        print(f"💰 Reward for this text: {reward} {coin_name}")
        return True
