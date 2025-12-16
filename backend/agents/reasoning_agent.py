import re
from agents.executor_agent import get_llm
from agents.planner_agent import (
    SUMMARY_PROMPT,
    FINAL_SUMMARY_PROMPT,
    BULLET_SUMMARY_PROMPT
)


def summarize_chunk(text: str) -> str:
    llm = get_llm(temperature=0.1, max_tokens=400)
    chain = SUMMARY_PROMPT | llm
    return chain.invoke({"text": text}).content


def merge_and_refine(paragraphs: list[str]) -> str:
    llm = get_llm(
        temperature=0.0,
        max_tokens=200
    )

    chain = FINAL_SUMMARY_PROMPT | llm

    raw = chain.invoke({
        "raw_summary": "\n\n".join(paragraphs)
    }).content

    # Extract numbered sentences safely
    sentences = re.findall(r'\d+\.\s*(.+?\.)', raw)

    # Join into final paragraph
    return " ".join(sentences[:3])




def paragraph_to_bullets(paragraph: str) -> str:
    """
    Converts a summary paragraph into bullet points
    WITHOUT introducing new information.
    """
    # Split into sentences safely
    sentences = re.split(r'(?<=[.!?])\s+', paragraph.strip())

    bullets = []
    for s in sentences:
        s = s.strip()
        if len(s) > 20:  # ignore tiny fragments
            bullets.append(f"- {s}")

    return "\n".join(bullets[:6])  # limit to 4–6 bullets


def reason_over_context(context_chunks: list[str]) -> str:
    """
    Combines retrieved context chunks into a single reasoning context
    for the chatbot. This is NOT used for summarization.
    """
    return "\n\n".join(context_chunks)
