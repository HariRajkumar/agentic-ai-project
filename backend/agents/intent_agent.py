from agents.executor_agent import get_llm


def merge_summaries(chunk_summaries: list[str]) -> str:
    llm = get_llm(temperature=0.1)

    joined = "\n\n".join(chunk_summaries)

    prompt = f"""
You are a senior technical summarization agent.

Combine the following partial summaries into ONE coherent final summary.
- Remove redundancy
- Preserve key points
- Use bullet points where appropriate

Partial summaries:
{joined}

Final Summary:
"""

    response = llm.invoke(prompt)
    return response.content

def analyze_intent(question: str) -> str:
    q = question.lower()

    if any(word in q for word in ["summarize", "overview", "brief"]):
        return "summary"

    if any(word in q for word in ["why", "how", "explain"]):
        return "explanation"

    if any(word in q for word in ["list", "components", "types"]):
        return "list"

    return "fact"
