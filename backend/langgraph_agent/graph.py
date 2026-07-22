from langgraph.graph import StateGraph, END
from backend.langgraph_agent.state import LoanBotState
from backend.langgraph_agent.nodes import (
    router_node,
    sales_node,
    verification_node,
    underwriting_node,
    sanction_node,
)
from backend.langgraph_agent.memory import memory_store


g = StateGraph(LoanBotState)

g.add_node("router", router_node)
g.add_node("sales", sales_node)
g.add_node("verification", verification_node)
g.add_node("underwriting", underwriting_node)
g.add_node("sanction", sanction_node)

g.set_entry_point("router")

g.add_conditional_edges(
    "router",
    lambda state: state["next"],
    {
        "sales": "sales",
        "verification": "verification",
        "underwriting": "underwriting",
        "sanction": "sanction",
    }
)

g.add_edge("sales", END)
g.add_edge("verification", END)
g.add_edge("underwriting", END)
g.add_edge("sanction", END)

graph = g.compile()


def run_langgraph_agent(user_input: str, session_id: str = "default") -> str:
    try:
        memory_store.add_user(session_id, user_input)

        state = {
            "session_id": session_id,
            "user_query": user_input,
            "messages": memory_store.get(session_id),
            "domain": "",                   # router will set this each turn
            "retrieved_passages": [],
            "rag_context": "",
            "final_response": "",
            "next": "",
            "uploaded_file": None,
            "upload_verified": None,
        }
        result = graph.invoke(state)
        print(f"[DEBUG] domain={result.get('domain')} | node={result.get('next')}")

        return result.get("final_response", "I could not generate a response.")
    except Exception as e:
        print(f"[LangGraph Error] {e}")
        return "An error occurred while routing your request via LangGraph."