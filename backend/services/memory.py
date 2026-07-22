from langchain_core.messages import AIMessage, HumanMessage

class MemoryService:
    def __init__(self):
        self.sessions = {}

    def add_user(self, session_id: str, text: str):
        self.sessions.setdefault(session_id, []).append(
            HumanMessage(content=text)
        )

    def add_ai(self, session_id: str, text: str):
        self.sessions.setdefault(session_id, []).append(
            AIMessage(content=text)
        )

    def get_history(self, session_id: str):
        return self.sessions.get(session_id, [])

    def clear(self, session_id: str):
        self.sessions[session_id] = []