# backend/worker_agents/sanction_agent.py

from datetime import date

def sanction_agent(query: str) -> str:
    """Generate a sanction letter for approved loans."""
    today = date.today().strftime("%d-%m-%Y")
    letter = f"""
    📄 Loan Sanction Letter
    ----------------------------------
    Date: {today}

    Dear Customer,

    We are pleased to inform you that your loan application has been approved.
    Loan Amount: ₹5,00,000
    Interest Rate: 10.5% per annum
    Tenure: 5 years
    EMI: ₹10,789 per month

    Kindly review the attached terms and proceed with documentation.

    Regards,
    Loan Processing Department
    """
    return letter.strip()
