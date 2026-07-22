from typing import TypedDict, List, Optional
from langchain_core.messages import BaseMessage


class LoanBotState(TypedDict):
    # --- Core ---
    session_id: str                      # identifies the user session
    user_query: str                      # current user message

    # --- Routing ---
    next: str                            # which node to go to next
    domain: str                          # "sales" / "verification" / "underwriting" / "sanction"
                                         # persists so follow-up questions know the topic

    # --- RAG ---
    retrieved_passages: List[str]        # what ChromaDB returned for this turn
    rag_context: str                     # formatted passages string passed to LLM

    # --- Memory ---
    messages: List[BaseMessage]          # full conversation history for this session

    # --- Response ---
    final_response: str                  # LLM reply sent back to user

    # --- Document upload ---
    uploaded_file: Optional[str]         # filename if user uploaded a document
    upload_verified: Optional[bool]      # whether verification passed