import re
from typing import Literal

DocType = Literal["coding", "concept", "other"]

CODING_HINTS = [
    "leetcode", "two sum", "binary search", "valid parentheses", "merge two",
    "linked list", "array", "string", "hash map", "stack", "queue",
    "time complexity", "space complexity", "big o", "runtime",
    "implement", "write code", "python", "return", "function",
    "edge case", "test case", "debug", "optimize", "complexity",
]

CONCEPT_HINTS = [
    "self-attention", "attention", "multi-head", "positional encoding",
    "transformer", "encoder", "decoder", "layernorm", "residual",
    "embedding", "cosine similarity", "rag", "retrieval", "vector database",
    "finetune", "fine-tune", "lora", "qlora",
    "mechanism", "intuition", "trade-off", "limitations", "why", "how does",
]

CHITCHAT_HINTS = [
    "hello", "hi", "hey", "thanks", "thank you", "good morning", "good night",
    "how are you", "what's up", "who are you",
]


def route_type(question: str) -> DocType:
    q = question.strip().lower()

    # Very short / greetings => other
    if len(q) <= 12 or q in CHITCHAT_HINTS:
        return "other"

    # Strong coding signals: code blocks / function signatures / typical constraints
    if "```" in q or re.search(r"\bdef\s+\w+\(", q) or "class " in q:
        return "coding"

    coding_score = sum(1 for w in CODING_HINTS if w in q)
    concept_score = sum(1 for w in CONCEPT_HINTS if w in q)

    # Extra heuristics
    if "code" in q or "implement" in q or "write" in q:
        coding_score += 2
    if q.startswith("what is") or q.startswith("explain") or q.startswith("why") or q.startswith("how"):
        concept_score += 1

    if coding_score == 0 and concept_score == 0:
        # Unknown/general question
        return "other"

    if coding_score > concept_score:
        return "coding"
    if concept_score > coding_score:
        return "concept"

    # Tie-break: if mentions python/code -> coding else concept
    if "python" in q or "code" in q:
        return "coding"
    return "concept"