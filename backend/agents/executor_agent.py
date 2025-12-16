from langchain_groq import ChatGroq
from config import Config
from agents.planner_agent import PLANNED_PROMPT


def get_llm(temperature: float = 0.1, max_tokens: int = 1024):
    """
    Shared LLM factory used across the system
    """
    return ChatGroq(
        api_key=Config.GROQ_API_KEY,
        model_name="llama-3.1-8b-instant",
        temperature=temperature,
        max_tokens=max_tokens
    )


def execute_response(
    context: str,
    question: str,
    intent: str,
    memory: str
) -> str:
    """
    Executes the final chatbot response using the planned prompt.
    """
    llm = get_llm(temperature=0.1, max_tokens=1024)

    chain = PLANNED_PROMPT | llm

    response = chain.invoke({
        "context": context,
        "question": question,
        "intent": intent,
        "memory": memory
    })

    return response.content
