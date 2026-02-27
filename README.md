# Interview Copilot (RAG + Multi-Turn Memory AI Agent)

An interview practice AI agent that combines:

- Retrieval-Augmented Generation (RAG)
- Automatic question type routing (coding / concept / other)
- Structured output schema enforcement
- Multi-turn conversational memory
- Knowledge-grounded answering with confidence control

Designed as a lightweight, modular, reproducible AI agent system.

---

## 🚀 Features

### 1. Automatic Question Routing
The system automatically classifies user questions into:

- `coding`
- `concept`
- `other` (general chat / non-knowledge-base questions)

This prevents unnecessary retrieval and improves response quality.

---

### 2. Retrieval-Augmented Generation (RAG)

For `coding` and `concept` questions:

1. Encode query using SentenceTransformers
2. Retrieve top-k relevant chunks from ChromaDB
3. Re-rank sections by semantic relevance + preferred section order
4. Inject retrieved context into LLM prompt
5. Generate structured answer

This reduces hallucination and grounds responses in the local knowledge base.

---

### 3. Structured Output Enforcement

All interview-style answers follow a strict output schema:

- Coding:
  - Result Snapshot
  - Quick Idea
  - Approach
  - Python Code
  - Complexity
  - Pitfalls
  - Self-check
  - Follow-up

- Concept:
  - Result Snapshot
  - Definition
  - Intuition
  - Mechanism
  - Example
  - Trade-offs
  - Common Misconceptions
  - Follow-up

The schema is injected into the system prompt and strictly enforced.

---

### 4. Multi-Turn Conversational Memory

The system maintains:

- Short-term memory (last N turns)
- Optional long-term summarized memory

This enables:
- Follow-up questions
- Clarifications
- Progressive refinement
- Context continuity

Memory size is bounded to prevent token explosion.

---

### 5. Confidence Threshold (Anti-Hallucination)

If top retrieval similarity score is too weak:

- The system refuses to fabricate answers
- It asks the user to extend the knowledge base
- Prevents unreliable hallucinated output

This mimics production-level RAG behavior.

---

## 🏗 System Architecture

User Input
    ↓
Router (coding / concept / other)
    ↓
If coding/concept:
    → Embed query
    → Retrieve from Chroma
    → Re-rank sections
    → Inject context
    → LLM generation (schema enforced)
Else:
    → Direct LLM response (no RAG)

All responses optionally pass through:
    → Memory summarization layer

---

## 🧠 Technologies Used

- Python
- OpenAI API (LLM generation)
- SentenceTransformers (embedding model)
- ChromaDB (vector database)
- Markdown-based local knowledge base
- Modular prompt construction
- Heuristic + rule-based router

---

## 📂 Project Structure

```
src/
  chat_app.py          # Main multi-turn agent entry
  rag/
    router.py          # Question classification
    retriever.py       # Embedding + Chroma retrieval
    prompts.py         # Prompt construction logic
    build_index.py     # Index builder

data/
  algorithm/           # Coding interview notes
  concept/             # ML/Transformer notes

docs/
  output_schema.md
  rag_design.md
```

---

## ⚙️ Setup

### 1. Install Dependencies

```
pip install -r requirements.txt
```

### 2. Build Vector Index

```
python -m src.rag.build_index
```

### 3. Set API Key

```
export OPENAI_API_KEY="your_key"
```

(Optional)
```
export OPENAI_MODEL="gpt-4o"
```

### 4. Run Agent

```
python -m src.chat_app --use_summary --show_router
```

---

## 🧪 Example Interaction

```
You: Explain positional encoding
[router] type=concept
→ Retrieved context
→ Structured explanation returned

You: Now give me the formula again
→ Multi-turn memory preserved
→ Context-aware follow-up
```

---

## 📈 Design Decisions

### Why Markdown Knowledge Base?
- Easy to expand
- Human-readable
- Version-controllable
- Flexible schema per topic

### Why Hybrid Router?
- Reduces unnecessary vector queries
- Improves latency
- Separates general chat from interview logic

### Why Confidence Threshold?
- Prevents hallucinated answers
- Encourages knowledge-grounded expansion
- Mimics production RAG safeguards

---

## 🔮 Future Improvements

- Replace heuristic router with small classifier model
- Add citation markers for retrieved chunks
- Add streaming token output
- Add web interface (Streamlit / FastAPI)
- Add evaluation pipeline (precision@k, answer grading)
- Add automatic knowledge gap detection
- Integrate tool-calling (e.g., code execution sandbox)

---

## 🎯 Resume Highlight Version

Built a multi-turn AI interview copilot using RAG architecture with automatic question routing, structured schema enforcement, Chroma vector retrieval, confidence thresholding, and long-term memory summarization to reduce hallucination and improve answer reliability.

---

## 📌 Notes

This project focuses on modular AI agent design, clean RAG architecture, and engineering-level reliability rather than building a large model from scratch.
