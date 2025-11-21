from backend.master_agent import run_master_agent

query = "What is the minimum salary for a home loan?"
response = run_master_agent(query)
print("Response:", response)
