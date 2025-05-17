from datetime import datetime

def analyze_risk(policyholders):
    risky = []
    now = datetime.now()
    for holder in policyholders:
        claims = holder.claims
        recent = [c for c in claims if datetime.strptime(c["date"], "%Y-%m-%d").year == now.year]
        total_claimed = sum(c["amount"] for c in claims)
        if len(recent) > 3 or total_claimed > 0.8 * holder.sum_insured:
            risky.append(holder)
    return risky
