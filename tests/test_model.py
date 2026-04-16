from app.model import LoanApplication

def test_loan_application_str():
    loan = LoanApplication("1", 1000, 2000)
    result = str(loan)

    assert "1" in result
    assert "1000" in result
    assert "2000" in result