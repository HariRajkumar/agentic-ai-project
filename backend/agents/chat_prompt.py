from langchain_core.prompts import PromptTemplate

CHAT_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are an AI assistant answering questions strictly based on the provided context.

Rules:
- Use ONLY the context below
- If the answer is not present, say "I don't have enough information"
- Be concise and clear
- Do not hallucinate

Context:
{context}

User Question:
{question}

Answer:
"""
)
