
from agents.risk_scorer import risk_scorer
import re

def requires_human_approval(risk_score: str) -> bool:
    match = re.search(r'(\d+(?:\.\d+)?)', risk_score)
    if match:
        score = float(match.group(1))
        return score >= 8
    return False

def get_human_approval(report: str) -> bool:
    print(report)
    while True:
        response = input("Approve this report? (yes/no): ").strip().lower()
        if response == "yes":
            return True
        elif response == "no":
            return False