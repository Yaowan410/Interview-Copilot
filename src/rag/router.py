import re
from typing import Literal

DocType = Literal["coding", "concept"]


CODING_HINTS = [
    "leetcode", "two sum", "binary search", "valid parentheses", "merge two",
    "linked list", "array", "string", "hash map", "stack", "queue",
    "time complexity", "space complexity", "big o", "runtime",
    "implement", "write code", "python", "return", "function",
    "edge case", "test case",
]

CONCEPT_HINTS = [
    "self-attention", "attention", "multi-head", "positional encoding",
    "transformer", "encoder", "decoder", "layernorm", "residual",
    "embedding", "cosine similarity", "rag", "retrieval", "vector database",
    "finetune", "lora", "qlora",
    "why", "how does", "mechanism", "intuition", "trade-off", "limitations",
]


def route_type(question: str) -> DocType:
    q = question.strip().lower()

    # Strong signals: code blocks / function signatures
    if "```" in q or re.search(r"\bdef\s+\w+\(", q):
        return "coding"

    # Keyword scoring
    coding_score = sum(1 for w in CODING_HINTS if w in q)
    concept_score = sum(1 for w in CONCEPT_HINTS if w in q)

    # Light heuristics
    if "code" in q or "implement" in q:
        coding_score += 2
    if q.startswith("what is") or q.startswith("explain"):
        concept_score += 1

    if coding_score > concept_score:
        return "coding"
    if concept_score > coding_score:
        return "concept"

    # Default fallback
    return "coding"