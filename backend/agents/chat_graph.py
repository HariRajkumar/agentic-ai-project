from langgraph.graph import StateGraph
from typing import TypedDict

from agents.intent_agent import analyze_intent
from agents.retrieval_agent import retrieve_context
from agents.reasoning_agent import reason_over_context
from agents.executor_agent import execute_response
from agents.memory import ConversationMemory
from db.chat_repository import add_message


class ChatState(TypedDict):
    question: str
    intent: str
    context_chunks: list[str]
    context: str
    answer: str


def create_chat_graph(session_id: str):
    graph = StateGraph(ChatState)
    memory = ConversationMemory(session_id)

    def intent_node(state):
        # ✅ Persist user message
        add_message(session_id, "user", state["question"])
        return {"intent": analyze_intent(state["question"])}

    def retrieval_node(state):
        return {"context_chunks": retrieve_context(state["question"])}

    def reasoning_node(state):
        return {"context": reason_over_context(state["context_chunks"])}

    def execution_node(state):
        answer = execute_response(
            context=state["context"],
            question=state["question"],
            intent=state["intent"],
            memory=memory.get_context()
        )

        # ✅ Persist assistant response
        add_message(session_id, "assistant", answer)

        return {"answer": answer}

    graph.add_node("intent", intent_node)
    graph.add_node("retrieve", retrieval_node)
    graph.add_node("reason", reasoning_node)
    graph.add_node("execute", execution_node)

    graph.set_entry_point("intent")
    graph.add_edge("intent", "retrieve")
    graph.add_edge("retrieve", "reason")
    graph.add_edge("reason", "execute")

    return graph.compile()
