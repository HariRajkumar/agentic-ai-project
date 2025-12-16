from agents.executor_agent import get_llm
from agents.chat_prompt import CHAT_PROMPT


def answer_question(context_chunks: list[str], question: str) -> str:
    llm = get_llm(temperature=0.1)

    context_text = "\n\n".join(context_chunks)

    chain = CHAT_PROMPT | llm
    response = chain.invoke({
        "context": context_text,
        "question": question
    })

    return response.content
