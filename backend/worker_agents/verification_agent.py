# backend/worker_agents/verification_agent.py

import pandas as pd
import os

# Simulated CRM dataset (you can replace this later with a real DB)
CUSTOMER_DB = os.path.join("backend", "data", "customers.csv")

# Example CSV structure:
# name,email,pan_number,kyc_status
# Divya,divya@gmail.com,ABCDE1234F,Verified
# Rohan,rohan@gmail.com,WXYZE9876G,Pending

def verification_agent(query: str) -> str:
    """Check customer's KYC or CRM record."""
    if not os.path.exists(CUSTOMER_DB):
        return "No customer data found. Please upload customer details."

    df = pd.read_csv(CUSTOMER_DB)

    for _, row in df.iterrows():
        if row["name"].lower() in query.lower() or row["email"].lower() in query.lower():
            status = row["kyc_status"]
            return f"KYC status for {row['name']}: {status}."

    return "Customer record not found in CRM database."
