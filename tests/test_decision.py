from app.graph import evaluate


def test_high_salary_approved():
    msg = "LoanRequest(applicationId=1, amount=20000, salary=10000)"
    result = evaluate(msg)

    assert result["decision"] == "APPROVED"
    assert result["risk_score"] < 0.5


def test_high_amount_rejected():
    msg = "LoanRequest(applicationId=1, amount=60000, salary=10000)"
    result = evaluate(msg)

    assert result["decision"] == "REJECTED"
    assert result["risk_score"] > 0.8


def test_medium_case_approved():
    msg = "LoanRequest(applicationId=1, amount=10000, salary=5000)"
    result = evaluate(msg)

    assert result["decision"] == "APPROVED"


def test_invalid_message():
    msg = "invalid_message"
    result = evaluate(msg)

    assert result["decision"] == "REJECTED"