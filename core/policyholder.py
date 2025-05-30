class Policyholder:
    def __init__(self, id, name, age, gender, policy_type, sum_insured, claims=None):
        self.id = id
        self.name = name
        self.age = age
        self.gender = gender
        self.policy_type = policy_type
        self.sum_insured = sum_insured
        self.claims = claims if claims else []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "policy_type": self.policy_type,
            "sum_insured": self.sum_insured,
            "claims": self.claims
        }
