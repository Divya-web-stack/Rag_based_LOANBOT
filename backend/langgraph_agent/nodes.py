from backend.langgraph_agent.memory import memory_store
from backend.rag_chromadb import query_docs
from langchain_core.messages import HumanMessage, AIMessage

# ---------------------------------------------------------------------------
# LLM initialisation
# ---------------------------------------------------------------------------
try:
    from langchain_ollama import OllamaLLM
    llm = OllamaLLM(model="gemma3:4b")
except ImportError:
    llm = None
    print("Warning: langchain-ollama not installed. Run: pip install -U langchain-ollama")


def format_message_history(messages: list) -> str:
    if not messages:
        return ""
    lines = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            lines.append(f"User: {msg.content}")
        elif isinstance(msg, AIMessage):
            lines.append(f"Assistant: {msg.content}")
        else:
            lines.append(str(msg))
    return "\n".join(lines)


def build_prompt(user_query: str, passages: list, history: list = None) -> str:
    history_text = format_message_history(history or [])
    history_block = f"Conversation history:\n{history_text}\n\n" if history_text else ""
    ctx_text = "\n\n---\n".join(passages) if passages else "No relevant policy found."

    return (
        "You are LoanBot — a strict banking assistant for loan/product policies.\n\n"
        "RULES YOU MUST FOLLOW:\n"
        "1. Base your answer ONLY on the policy context provided below.\n"
        "2. If the user does NOT meet a policy criterion (age, income, etc.), clearly tell them they are NOT eligible. Never agree when criteria are not met.\n"
        "3. If the answer is not in the policy context, say: 'I don\'t have that information. Please contact our support team.\'\n"
        "4. Do NOT invent forms, URLs, phone numbers, or processes not mentioned in the policy.\n"
        "5. Do NOT include raw policy citations like \'Policy Context:\' or \'Passage X\' in your reply.\n"
        "6. Keep answers concise and factual.\n\n"
        f"{history_block}"
        f"Policy context (most relevant passages):\n{ctx_text}\n\n"
        f"User question: {user_query}\n\n"
        "Answer strictly based on the policy context above."
    )


# ---------------------------------------------------------------------------
# Context-aware router
# ---------------------------------------------------------------------------
# Short follow-up phrases that should never trigger a domain change
STICKY_PHRASES = {
    "yes", "yes please", "sure", "okay", "ok", "go ahead",
    "tell me more", "please", "continue", "more", "elaborate",
    "explain", "got it", "i see", "alright", "sounds good"
}

def router_node(state: dict) -> dict:
    """
    Routes based on:
    1. If message is a vague follow-up → LOCK current domain (never re-route)
    2. Current message keywords (high priority)
    3. domain already set in state from previous turn
    4. Recent AI replies in memory (last resort)
    """
    text = state["user_query"].lower().strip()
    current_domain = state.get("domain", "")

    # --- Lock domain for vague follow-ups (yes/sure/ok/tell me more etc.) ---
    # These should NEVER cause a domain switch regardless of AI reply keywords
    is_sticky = (
        text in STICKY_PHRASES
        or len(text.split()) <= 2
        or text.startswith("i am")
        or text.startswith("i earn")
        or text.startswith("i have")
        or text.startswith("i am a")
    )
    if is_sticky and current_domain:
        print(f"[ROUTER] sticky follow-up '{text}' → locked to domain={current_domain}")
        return {"next": current_domain, "domain": current_domain}

    # --- Current message keywords (high priority) ---
    if any(k in text for k in ["pan", "aadhaar", "kyc", "document", "verify"]):
        return {"next": "verification", "domain": "verification"}

    if any(k in text for k in ["eligible", "eligibility", "qualify", "income", "salary", "criteria"]):
        return {"next": "underwriting", "domain": "underwriting"}

    if any(k in text for k in ["approve", "approval", "sanction", "disburse", "disbursement"]):
        return {"next": "sanction", "domain": "sanction"}

    # --- Follow-up: use domain stored in state from last turn ---
    if current_domain in ("verification", "underwriting", "sanction", "sales"):
        return {"next": current_domain, "domain": current_domain}

    # --- Last resort: check recent AI memory context ---
    history = memory_store.get(state["session_id"])
    recent_context = " ".join([
        m.content.lower()
        for m in history[-6:]
        if isinstance(m, AIMessage)
    ])

    if any(k in recent_context for k in ["pan", "aadhaar", "kyc", "document", "verify"]):
        return {"next": "verification", "domain": "verification"}

    if any(k in recent_context for k in ["eligible", "eligibility", "qualify", "income", "salary"]):
        return {"next": "underwriting", "domain": "underwriting"}

    if any(k in recent_context for k in ["approve", "approval", "sanction", "disburse"]):
        return {"next": "sanction", "domain": "sanction"}

    return {"next": "sales", "domain": "sales"}


# ---------------------------------------------------------------------------
# Shared LLM caller
# ---------------------------------------------------------------------------
def call_llm(prompt: str) -> str:
    try:
        raw = llm.invoke(prompt) if hasattr(llm, "invoke") else llm(prompt)
        return raw if isinstance(raw, str) else str(raw)
    except Exception as e:
        print(f"LLM call failed: {e}")
        return "Sorry, I couldn't process your request right now. Please try again later."


# ---------------------------------------------------------------------------
# Generic RAG node — now writes retrieved_passages and rag_context to state
# ---------------------------------------------------------------------------
def _rag_node(state: dict, k: int = 3) -> dict:
    session_id = state["session_id"]
    user_input = state["user_query"]

    # Enrich vague short queries with domain + last AI topic for better ChromaDB hits
    # e.g. "yes please" + domain="sanction" -> "sanction <last topic> yes please"
    domain = state.get("domain", "")
    is_vague = len(user_input.split()) <= 3
    if is_vague and domain:
        history = memory_store.get(session_id)
        last_ai = next(
            (m.content for m in reversed(history) if isinstance(m, AIMessage)), ""
        )
        topic_hint = " ".join(last_ai.split()[:10]) if last_ai else ""
        enriched_query = f"{domain} {topic_hint} {user_input}".strip()
        print(f"[RAG] vague query enriched: '{user_input}' -> '{enriched_query}'")
    else:
        enriched_query = user_input

    # 1. Retrieve from ChromaDB using enriched query
    passages = query_docs(enriched_query, k=k)

    # 2. Build prompt with fresh memory history (show original query to LLM, not enriched)
    history = memory_store.get(session_id)
    prompt = build_prompt(user_input, passages, history)

    # 3. Call LLM
    reply = call_llm(prompt)

    # 4. Save AI reply to memory
    memory_store.add_ai(session_id, reply)

    # 5. Return full state patch
    return {
        "messages": memory_store.get(session_id),
        "retrieved_passages": passages,
        "rag_context": "\n\n---\n".join(passages),
        "final_response": reply,
    }


# ---------------------------------------------------------------------------
# Domain nodes
# ---------------------------------------------------------------------------
def sales_node(state: dict) -> dict:
    return _rag_node(state, k=4)

def verification_node(state: dict) -> dict:
    return _rag_node(state, k=3)

def underwriting_node(state: dict) -> dict:
    return _rag_node(state, k=3)

def sanction_node(state: dict) -> dict:
    return _rag_node(state, k=3)