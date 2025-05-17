class Policyholder:
    def __init__(self, pid, name, age, policy_type, sum_insured):
        self.id = pid
        self.name = name
        self.age = age
        self.policy_type = policy_type
        self.sum_insured = sum_insured
        self.claims = []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "policy_type": self.policy_type,
            "sum_insured": self.sum_insured,
            "claims": self.claims,
        }
