from db.chat_repository import get_messages


class ConversationMemory:
    def __init__(self, session_id: str, max_turns: int = 6):
        self.session_id = session_id
        self.max_turns = max_turns

    def get_context(self) -> str:
        messages = get_messages(self.session_id, limit=self.max_turns * 2)

        lines = []
        for msg in messages:
            prefix = "User" if msg["role"] == "user" else "Assistant"
            lines.append(f"{prefix}: {msg['content']}")

        return "\n".join(lines)
