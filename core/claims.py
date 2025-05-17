from datetime import datetime

def create_claim(policyholders, claim_id, holder_id, amount, reason, status, date):
    for holder in policyholders:
        if holder.id == holder_id:
            holder.claims.append({
                "claim_id": claim_id,
                "amount": amount,
                "reason": reason,
                "status": status,
                "date": date,
            })
            return True
    return False
