import json
from core.policyholder import Policyholder

def save_data(policyholders, filename="data/data.json"):
    with open(filename, "w") as f:
        json.dump([p.to_dict() for p in policyholders], f)

def load_data(filename="data/data.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        return [Policyholder(**p) for p in data]
    except FileNotFoundError:
        return []
