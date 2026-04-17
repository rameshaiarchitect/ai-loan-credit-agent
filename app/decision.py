import re

def parse_agent(message: str):
    amount_match = re.search(r"amount=(\d+\.?\d*)", message)
    salary_match = re.search(r"salary=(\d+\.?\d*)", message)

    if not amount_match or not salary_match:
        return {"error": "Invalid input"}

    return {
        "amount": float(amount_match.group(1)),
        "salary": float(salary_match.group(1))
    }


def risk_agent(data: dict):
    if "amount" not in data or "salary" not in data:
        return {"risk_score": 1.0}

    ratio = data["amount"] / data["salary"]

    if ratio > 5:
        return {"risk_score": 0.9}

    if data["salary"] >= 8000:
        return {"risk_score": 0.2}

    if data["salary"] >= 4000 and ratio <= 3:
        return {"risk_score": 0.4}

    return {"risk_score": 0.7}


def fraud_agent(data: dict):
    if "amount" not in data:
        return {"fraud_flag": True}

    if data["amount"] > 50000:
        return {"fraud_flag": True}

    return {"fraud_flag": False}


def compliance_agent(data: dict):
    # Simulate AML / KYC rules
    if "amount" not in data:
        return {"compliance_flag": False}

    # Example rule: very high transactions need manual review
    if data["amount"] > 75000:
        return {"compliance_flag": False}

    # Otherwise compliant
    return {"compliance_flag": True}


def decision_agent(data: dict):
    if "amount" not in data or "salary" not in data:
        return {
            "decision": "REJECTED",
            "reason": "Invalid input"
        }

    # Fraud has highest priority
    if data.get("fraud_flag", False):
        return {
            "decision": "REJECTED",
            "reason": "Fraud detected"
        }
        
    # Compliance check
    if not data.get("compliance_flag", True):
        return {
            "decision": "REJECTED",
            "reason": "Compliance check failed"
        }

    if data.get("risk_score", 1.0) >= 0.8:
        return {
            "decision": "REJECTED",
            "reason": "High risk"
        }

    if data.get("risk_score", 1.0) <= 0.4:
        return {
            "decision": "APPROVED",
            "reason": "Low risk"
        }

    return {
        "decision": "REJECTED",
        "reason": "Medium risk"
    }