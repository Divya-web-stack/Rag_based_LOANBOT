# backend/worker_agents/underwriting_agent.py

def underwritting_agent(query: str) -> str:
    """Apply simple eligibility rules based on loan criteria."""
    # Simple keyword-based rule mock
    if "salary" in query.lower() or "income" in query.lower():
        return "For a personal loan, minimum net monthly income should be ₹25,000."
    elif "credit score" in query.lower():
        return "Applicants should have a minimum credit score of 700 for loan approval."
    elif "self-employed" in query.lower():
        return "Self-employed individuals must provide 2 years of ITR and business proof."
    else:
        return (
            "Loan eligibility depends on income, credit score, and employment type. "
            "Would you like to check eligibility for a specific case?"
        )
