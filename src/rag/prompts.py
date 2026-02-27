from pathlib import Path
from typing import Literal, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_SCHEMA_PATH = PROJECT_ROOT / "docs" / "output_schema.md"

DocType = Literal["coding", "concept", "other"]


def load_output_schema() -> str:
    if not OUTPUT_SCHEMA_PATH.exists():
        raise FileNotFoundError("docs/output_schema.md not found.")
    return OUTPUT_SCHEMA_PATH.read_text(encoding="utf-8", errors="ignore").strip()


def build_system_prompt(schema: str) -> str:
    return (
        "You are an Interview Practice Tutor.\n"
        "You must follow the required output schema EXACTLY.\n"
        "IMPORTANT OUTPUT RULES:\n"
        "1) Output ONLY the final answer. Do NOT repeat the schema text. Do NOT print 'Retrieved Context'.\n"
        "2) Use Markdown headings EXACTLY as written in the schema, including leading ###.\n"
        "3) For coding questions, include runnable Python code inside a ```python code block.\n"
        "4) Ground your answer in the retrieved context when provided. If context is insufficient, say so briefly and continue.\n"
        "\n"
        "Required Output Schema:\n"
        f"{schema}\n"
    )


def build_user_message(doc_type: DocType, question: str, context: str = "", memory: str = "") -> str:
    """
    - other: no RAG context attached (pure chat / general guidance)
    - coding/concept: include retrieved context
    """
    if doc_type == "other":
        return (
            f"Long-term Memory (if any):\n{memory if memory else '(none)'}\n\n"
            f"User Question:\n{question}\n"
        )

    # coding / concept
    return (
        f"Long-term Memory (if any):\n{memory if memory else '(none)'}\n\n"
        f"Doc type: {doc_type}\n\n"
        f"Retrieved Context:\n{context}\n\n"
        f"User Question:\n{question}\n"
    )


def build_other_style_hint() -> str:
    """
    For 'other' questions, we don't want it to force the interview schema.
    We'll use a different system instruction just for that path.
    """
    return (
        "You are a helpful technical assistant.\n"
        "For general questions, answer naturally and concisely.\n"
        "If the user asks for interview-style structure, you may use headings, but do not force the interview schema.\n"
    )