import os
import pickle

DATA_FILE = "data/policyholders.pkl"

def save_data(policyholders):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "wb") as f:
        pickle.dump(policyholders, f)

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "rb") as f:
        return pickle.load(f)
