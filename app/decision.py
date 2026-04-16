def decide(application_str: str) -> str:
    if "amount=" in application_str and "salary=" in application_str:
        return "APPROVED"
    return "REJECTED"