from app.consumer import process_message, create_consumer

def test_process_message_approved():
    msg = "LoanRequest(applicationId=1, amount=1000, salary=2000)"
    assert process_message(msg) == "APPROVED"

def test_process_message_rejected():
    msg = "invalid_message"
    assert process_message(msg) == "REJECTED"

def test_create_consumer():
    consumer = create_consumer()
    assert consumer is not None