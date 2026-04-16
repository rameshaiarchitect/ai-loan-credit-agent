class LoanApplication:
    def __init__(self, application_id: str, amount: int, salary: int):
        self.application_id = application_id
        self.amount = amount
        self.salary = salary

    def __str__(self):
        return f"{self.application_id}:{self.amount}:{self.salary}"