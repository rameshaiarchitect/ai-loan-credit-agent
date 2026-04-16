from app.decision import decide

def test_decide_approved():
    msg = "LoanRequest(applicationId=1, amount=1000, salary=2000)"
    assert decide(msg) == "APPROVED"

def test_decide_rejected():
    msg = "invalid_message"
    assert decide(msg) == "REJECTED"