from langgraph.graph import StateGraph
from typing import TypedDict, List

from rag.chunking import chunk_text
from agents.reasoning_agent import summarize_chunk, merge_and_refine


class SummaryState(TypedDict):
    text: str
    chunks: List[str]
    chunk_paragraphs: List[str]
    final_summary: str


def create_summarization_graph():
    graph = StateGraph(SummaryState)

    def chunk_node(state):
        return {"chunks": chunk_text(state["text"])}

    def summarize_chunks_node(state):
        return {
            "chunk_paragraphs": [
                summarize_chunk(chunk)
                for chunk in state["chunks"]
            ]
        }

    def final_summary_node(state):
        return {
            "final_summary": merge_and_refine(state["chunk_paragraphs"])
        }

    graph.add_node("chunk", chunk_node)
    graph.add_node("summarize_chunks", summarize_chunks_node)
    graph.add_node("final_summary", final_summary_node)

    graph.set_entry_point("chunk")
    graph.add_edge("chunk", "summarize_chunks")
    graph.add_edge("summarize_chunks", "final_summary")

    return graph.compile()
