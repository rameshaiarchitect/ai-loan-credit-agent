import re

def parse_loan(message: str):
    amount_match = re.search(r"amount=(\d+\.?\d*)", message)
    salary_match = re.search(r"salary=(\d+\.?\d*)", message)

    if not amount_match or not salary_match:
        return None, None

    return float(amount_match.group(1)), float(salary_match.group(1))


def evaluate(application_str: str):
    amount, salary = parse_loan(application_str)

    if amount is None or salary is None:
        return {
            "decision": "REJECTED",
            "risk_score": 1.0,
            "reason": "Invalid input"
        }

    ratio = amount / salary

    # Rule 1: Too risky
    if ratio > 5:
        return {
            "decision": "REJECTED",
            "risk_score": 0.9,
            "reason": "Loan amount too high compared to salary"
        }

    # Rule 2: Strong income
    if salary >= 8000:
        return {
            "decision": "APPROVED",
            "risk_score": 0.2,
            "reason": "High salary, low risk"
        }

    # Rule 3: Balanced case
    if salary >= 4000 and ratio <= 3:
        return {
            "decision": "APPROVED",
            "risk_score": 0.4,
            "reason": "Balanced loan-to-income ratio"
        }

    # Default
    return {
        "decision": "REJECTED",
        "risk_score": 0.7,
        "reason": "Insufficient financial strength"
    }