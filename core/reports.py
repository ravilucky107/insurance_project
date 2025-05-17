from collections import defaultdict
from datetime import datetime

def generate_reports(policyholders):
    monthly_totals = defaultdict(float)
    policy_type_avg = defaultdict(list)
    highest_claim = {"amount": 0}
    pending = []

    for holder in policyholders:
        for claim in holder.claims:
            month = datetime.strptime(claim["date"], "%Y-%m-%d").strftime("%Y-%m")
            monthly_totals[month] += claim["amount"]
            policy_type_avg[holder.policy_type].append(claim["amount"])

            if claim["amount"] > highest_claim.get("amount", 0):
                highest_claim = claim

            if claim["status"].lower() == "pending":
                pending.append(holder)

    avg_by_type = {k: sum(v)/len(v) for k, v in policy_type_avg.items()}
    return monthly_totals, avg_by_type, highest_claim, pending
