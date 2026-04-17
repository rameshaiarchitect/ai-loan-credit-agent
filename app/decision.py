from pydantic import BaseModel
from app.llm import get_llm


class DecisionOutput(BaseModel):
    decision: str
    reason: str


def decision_agent(data: dict):

    # ❌ invalid input
    if "amount" not in data or "salary" not in data:
        return {"decision": "REJECTED", "reason": "Invalid input"}

    # ✅ HARD RULES (STRICT ORDER)

    if data.get("fraud_flag"):
        return {"decision": "REJECTED", "reason": "Fraud detected"}

    if not data.get("compliance_flag", True):
        return {"decision": "REJECTED", "reason": "Compliance check failed"}

    # ✅ TEST MODE (deterministic)
    if data.get("test_mode"):
        if data.get("risk_score", 1.0) <= 0.4:
            return {"decision": "APPROVED", "reason": "Low risk"}
        return {"decision": "REJECTED", "reason": "High risk"}

    # 🤖 LLM MODE
    llm = get_llm()
    structured_llm = llm.with_structured_output(DecisionOutput)

    prompt = f"""
You are a credit decision system.

Input:
- Risk Score: {data.get('risk_score')}

Rules:
- If risk_score <= 0.4 → APPROVE
- Otherwise → REJECT

Return decision and reason.
"""

    try:
        response = structured_llm.invoke(prompt)

        decision = response.decision.upper()

        if decision == "APPROVE":
            decision = "APPROVED"
        elif decision == "REJECT":
            decision = "REJECTED"

        return {
            "decision": decision,
            "reason": response.reason
        }

    except Exception as e:
        return {
            "decision": "REJECTED",
            "reason": f"LLM failure: {str(e)}"
        }