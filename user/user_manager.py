# user/user_manager.py
import os
import json

USER_DIR = "data/users"

def register_user(username):
    os.makedirs(USER_DIR, exist_ok=True)
    filepath = os.path.join(USER_DIR, f"{username}.json")
    if os.path.exists(filepath):
        return False  # User already exists
    with open(filepath, "w") as f:
        json.dump({"username": username, "wallet": {}, "mined": []}, f)
    return True

def load_user(username):
    filepath = os.path.join(USER_DIR, f"{username}.json")
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r") as f:
        return json.load(f)

def save_user(user_data):
    filepath = os.path.join(USER_DIR, f"{user_data['username']}.json")
    with open(filepath, "w") as f:
        json.dump(user_data, f, indent=4)
