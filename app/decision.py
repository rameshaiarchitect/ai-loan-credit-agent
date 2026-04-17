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


from app.llm import get_llm


def decision_agent(data: dict):
    if "amount" not in data or "salary" not in data:
        return {
            "decision": "REJECTED",
            "reason": "Invalid input"
        }

    if data.get("test_mode"):
        if data.get("fraud_flag"):
            return {"decision": "REJECTED", "reason": "Fraud detected"}

        if not data.get("compliance_flag", True):
            return {"decision": "REJECTED", "reason": "Compliance check failed"}

        if data.get("risk_score", 1.0) <= 0.4:
            return {"decision": "APPROVED", "reason": "Low risk"}

        return {"decision": "REJECTED", "reason": "High risk"}

    # LLM mode
    llm = get_llm()

    prompt = f"""
    You are a credit decision system.

    Input:
    - Amount: {data.get('amount')}
    - Salary: {data.get('salary')}
    - Risk Score: {data.get('risk_score')}
    - Fraud Flag: {data.get('fraud_flag')}
    - Compliance Flag: {data.get('compliance_flag')}

    Rules:
    - If fraud_flag is True → REJECT
    - If compliance_flag is False → REJECT
    - Otherwise consider risk_score:
        - <= 0.4 → APPROVE
        - > 0.4 → REJECT

    Respond ONLY in format:
    Decision: <APPROVED/REJECTED>
    Reason: <short explanation>
    """

    response = llm.invoke(prompt).content

    decision = "REJECTED"
    reason = "Unknown"

    for line in response.splitlines():
        line = line.strip()

        if line.lower().startswith("decision:"):
            decision = line.split(":", 1)[1].strip().upper()

        elif line.lower().startswith("reason:"):
            reason = line.split(":", 1)[1].strip()

    return {
        "decision": decision,
        "reason": reason
    }