# backend/master_agent.py

from langchain_community.llms import Ollama
from langchain_community.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

# Import RAG retriever
from backend.rag_chromadb import query_docs

# Import worker agents
from backend.worker_agents.sales_agent import sales_agent
from backend.worker_agents.verification_agent import verification_agent
from backend.worker_agents.underwritting_agent import underwritting_agent
from backend.worker_agents.sanction_agent import sanction_agent

# -----------------------------------------------------------
# 1️⃣ Initialize Local LLM via Ollama (using Mistral)
# -----------------------------------------------------------
llm = Ollama(model="gemma3:4b")

# -----------------------------------------------------------
# 2️⃣ Define Specialized Worker Tools
# -----------------------------------------------------------
tools = [
    Tool(
        name="SalesAgent",
        func=sales_agent,
        description="Discuss loan offers and available products."
    ),
    Tool(
        name="VerificationAgent",
        func=verification_agent,
        description="Verify customer details and KYC using CRM data."
    ),
    Tool(
        name="UnderwritingAgent",
        func=underwritting_agent,
        description="Evaluate customer eligibility based on loan rules."
    ),
    Tool(
        name="SanctionAgent",
        func=sanction_agent,
        description="Generate sanction letters or approval documents."
    ),
]

# -----------------------------------------------------------
# 3️⃣ Load Prompt Template (ReAct prompt from LangChain Hub)
# -----------------------------------------------------------
try:
    prompt = hub.pull("hwchase17/react")
except Exception:
    prompt = "You are a helpful assistant that delegates tasks to worker agents as needed."

# -----------------------------------------------------------
# 4️⃣ Create Reasoning + Acting Agent
# -----------------------------------------------------------
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# -----------------------------------------------------------
# 5️⃣ Main Orchestrator Logic (Master Agent)
# -----------------------------------------------------------
def run_master_agent(user_input: str) -> str:
    """
    Run the main master agent that integrates:
      - RAG (retrieve relevant policy context from ChromaDB)
      - LLM reasoning (via Mistral)
      - Delegation to worker agents
    """
    try:
        # Step 1: Retrieve contextual data from knowledge base
        context = query_docs(user_input)
        context_text = f"Relevant policy information:\n{context}\n\n"

        # Step 2: Prepare structured query for the LLM
        full_query = (
            f"{context_text}User query: {user_input}\n"
            f"Use the worker agents if needed to complete this task."
        )

        # Step 3: Execute through agent reasoning pipeline
        result = agent_executor.invoke({"input": full_query})
        return result.get("output", "Sorry, I couldn't process that request.")

    except Exception as e:
        print(f"[MasterAgent Error] {e}")
        return "An error occurred while processing your request."




