from app.consumer import process_message

def test_process_message_approved():
    msg = "LoanRequest(applicationId=1, amount=10000, salary=5000)"
    result = process_message(msg)

    assert result["decision"] == "APPROVED"


def test_process_message_rejected():
    msg = "LoanRequest(applicationId=1, amount=1000, salary=2000)"
    result = process_message(msg)

    assert result["decision"] == "REJECTED"