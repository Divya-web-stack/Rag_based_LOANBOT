def check_eligibility(income, credit):
    if credit < 700:
        return "reject"
    elif income > 40000 and credit >= 750:
        return "approve"
    elif income > 25000:
        return "review"
    else:
        return "reject"
