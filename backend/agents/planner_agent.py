from langchain_core.prompts import PromptTemplate

# ---------- Summarization prompts ----------

SUMMARY_PROMPT = PromptTemplate(
    input_variables=["text"],
    template="""
You are summarizing a technical document chunk.

Rules:
- Write a concise paragraph
- Do NOT use bullet points
- Do NOT list methods
- Focus on purpose, structure, and intent
- Preserve important technical terms
- Complete all sentences

Content:
{text}

Summary paragraph:
"""
)

FINAL_SUMMARY_PROMPT = PromptTemplate(
    input_variables=["raw_summary"],
    template="""
Extract EXACTLY 3 complete summary sentences from the text below.

RULES:
- Each sentence must be self-contained and complete
- Each sentence must end with a period
- Do NOT combine sentences
- Do NOT expand ideas
- Do NOT explain details
- Output format MUST be:

1. <sentence>
2. <sentence>
3. <sentence>

Text:
{raw_summary}

Extracted sentences:
"""
)


BULLET_SUMMARY_PROMPT = PromptTemplate(
    input_variables=["paragraph"],
    template="""
You are converting an EXISTING summary paragraph into bullet points.

STRICT RULES (MANDATORY):
- Use ONLY the information present in the paragraph
- Do NOT add new concepts, examples, or explanations
- Do NOT generalize or infer intent
- Do NOT use vague enterprise language
- Each bullet must be directly traceable to a sentence in the paragraph
- Each bullet must be a complete sentence

Paragraph:
{paragraph}

Bullet points (faithful reformatting only):
"""
)


# ---------- Chatbot prompt ----------

PLANNED_PROMPT = PromptTemplate(
    input_variables=["context", "question", "intent", "memory"],
    template="""
You are an AI assistant answering a user question.

Conversation so far:
{memory}

Intent: {intent}

Rules:
- Use ONLY the provided context
- Do NOT invent facts
- If the answer is not in context, say so
- Structure response based on intent

Context:
{context}

Question:
{question}

Answer:
"""
)
