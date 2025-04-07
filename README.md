# AI-Powered-CryptoC
This project integrates blockchain, AI, and a dynamic economic strategy through our ocean equilibrium approach to create a sustainable and adaptive cryptocurrency ecosystem. The system leverages AI for content analysis—detecting both AI-generated and published content—and adjusts mining rewards accordingly.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Blockchain Usage](#blockchain-usage)
- [Ocean Equilibrium Strategy](#ocean-equilibrium-strategy)
- [Where AI Is Used](#where-ai-is-used)
- [Tech Stack](#tech-stack)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)

---

## Overview

The AI-Powered Blockchain Crypto Platform is an innovative backend solution that leverages blockchain technology and AI to build a self-regulating digital economy. Users can:

- **Create personal cryptocurrencies** and manage wallets.
- **Mine crypto** by submitting creative text or images. The system uses AI to detect AI-generated or published content and adjusts rewards accordingly.
- **Trade currencies** using an ocean equilibrium strategy that dynamically balances the ecosystem.
- **List and purchase content** on a marketplace with built-in copyright checks.
- **Share "treasure moments"** to highlight significant crypto earnings from creative contributions.

---

## Features

- **User-Defined Cryptocurrencies:** Create, manage, and trade your own coins.
- **AI-Powered Mining:**
  - **Text Mining:** Uses sentiment analysis and AI-detection to reward originality.
  - **Image Mining:** Leverages models (e.g., CLIP) for evaluating image content.
- **Adaptive Reward System:** Rewards adjust based on sentiment, text length, and user experience.
- **Published Content Detection:** Detects if content is AI-generated or already published online—if so, only a minimal reward is granted and such content is blocked from being listed.
- **Ocean Equilibrium Trading:** Dynamically balances the user's wallet by slightly reducing the value of other currencies when one currency gains value.
- **Marketplace:** List original content for sale and purchase content from other users.
- **Social Sharing:** Generate shareable messages for successful purchases and treasure moments.
- **Comprehensive Logging:** Trade and transaction events are logged for transparency and auditing.

---

## Blockchain Usage

Blockchain is at the core of this platform. Here's how it's used:

- **Immutable Transaction Records:**  
  Every mining event, trade, or listing is recorded as a transaction on a blockchain. Each block contains a batch of transactions that is cryptographically linked to the previous block, ensuring that data cannot be altered retroactively.

- **Personalized Blockchains:**  
  Each user-created cryptocurrency has its own blockchain (stored as JSON files) that logs all transactions (mining rewards, trades, etc.) related to that coin. This decentralized ledger maintains a verifiable history of all actions for each currency.

- **Rebalancing and Ocean Equilibrium:**  
  When trades or mining events occur, the blockchain records the adjustments made across the user's wallet. This ensures transparency in how the ocean equilibrium strategy (where gains in one currency reduce the value of others) is applied.

- **Adaptive Reward Logging:**  
  Mining rewards—calculated adaptively using AI—are stored in the blockchain. This not only maintains a secure record of rewards given but also provides data for the dynamic leaderboard and future adaptive learning improvements.

---

## Ocean Equilibrium Strategy

Our platform employs an **ocean equilibrium strategy** to maintain a balanced digital economy:

- **Dynamic Equilibrium:**  
  When a trade or mining event occurs, the system credits the currency being mined or traded while slightly reducing the value of other currencies in the wallet. This mimics natural ocean currents and ensures that no single currency becomes overly dominant.

- **Seesaw Effect:**  
  Just like a seesaw, an increase in one currency's value results in a slight decrease in others, promoting long-term stability and fairness in the ecosystem.

- **Adaptive Rewards:**  
  Mining rewards are dynamically adjusted based on factors like sentiment score, text length, and user experience. This adaptive mechanism encourages originality and quality.

*Example:*  
If a user’s wallet shows:
- **Pikachu:** 674.69  
- **Skycoin:** 466.6  
These values are the cumulative result of mining rewards and dynamic rebalancing adjustments from trades, ensuring overall stability.

---

## Where AI Is Used

- **Sentiment Analysis & AI-Detection:**  
  The platform uses Hugging Face Transformers to analyze the sentiment of submitted text and detect AI-generated content. This ensures that only high-quality, original content receives a substantial reward.

- **Published Content Detection:**  
  A search-based method (using DuckDuckGo and RapidFuzz) checks if text is already published online. If it is, a minimal reward is applied, and the content is blocked from marketplace listing.

- **Image Mining:**  
  AI models like CLIP are used to evaluate image content for mining, enabling visual creativity to be rewarded.

- **Adaptive Learning for Rewards:**  
  The system uses historical data (like number of uploads and mining events) to adjust rewards dynamically, ensuring fairness and promoting sustained quality.

---

## Tech Stack

| Layer             | Technology                              |
|-------------------|-----------------------------------------|
| Programming       | Python 3.11+                            |
| API Framework     | FastAPI                                 |
| Blockchain Logic  | Custom Python Modules (JSON-based)      |
| AI Models         | Hugging Face Transformers               |
| Data Storage      | JSON files (Prototype; scalable to DB)  |
| Logging           | Python `logging` module                 |
| Version Control   | Git and GitHub                          |

---

## API Endpoints

Some key endpoints (accessible via FastAPI’s interactive docs at /docs):

GET /wallet/{username} – Retrieve wallet balances.
POST /wallet/{username}/trade – Execute trades between cryptocurrencies.
POST /mine/text – Mine creative text content.
POST /mine/image – Mine image content.
GET /leaderboard – View cryptocurrency leaderboard.
POST /marketplace/list – List content on the marketplace.
GET /marketplace/search – Search listings by content title.
POST /marketplace/buy – Purchase marketplace content.
POST /share/moment – Share a treasure moment.
GET /shared/{user} – Retrieve a user’s shared moment.

## Installation Setup
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/himanshudhingra2910/AI-Powered-CryptoC.git
   cd AI-Powered-CryptoC

2. Setup Python Environment: It is recommended to use a Conda environment:
conda create -n crypto_env python=3.11
conda activate crypto_env
pip install -r requirements.txt

3.Run the API:
uvicorn api.main:app --reload


