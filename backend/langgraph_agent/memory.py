from typing import Dict, List
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

class SessionMemory:
    def __init__(self):
        self.sessions: Dict[str, List[BaseMessage]] = {}

    def get(self, session_id: str) -> List[BaseMessage]:
        return self.sessions.get(session_id, [])

    def add_user(self, session_id: str, text: str):
        self.sessions.setdefault(session_id, []).append(
            HumanMessage(content=text)
        )

    def add_ai(self, session_id: str, text: str):
        self.sessions.setdefault(session_id, []).append(
            AIMessage(content=text)
        )

    def clear(self, session_id: str):
        self.sessions[session_id] = []

# Initialize memory store instance
memory_store = SessionMemory()