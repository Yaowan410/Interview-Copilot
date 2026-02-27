import argparse
from pathlib import Path
from typing import Dict, List, Tuple

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


# -------- Paths / Settings --------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHROMA_DIR = PROJECT_ROOT / "chroma_db"
COLLECTION_NAME = "interview_copilot"
EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

OUTPUT_SCHEMA_PATH = PROJECT_ROOT / "docs" / "output_schema.md"


# -------- Preferred ordering of sections --------
CODING_SECTION_ORDER = [
    "Key Idea",
    "Step-by-Step Approach",
    "Python Template",
    "Complexity",
    "Edge Cases",
    "Common Mistakes",
    "Self-Check Examples",
    "Follow-Up",
    "Pattern",
    "Problem Summary",
]

CONCEPT_SECTION_ORDER = [
    "Result Snapshot",
    "Definition",
    "Intuition",
    "Mechanism",
    "Example",
    "Trade-offs",
    "Advantages",
    "Limitations",
    "Common Misconceptions",
    "Complexity",
    "Follow-Up Questions",
]

CODING_ORDER_MAP = {name: i for i, name in enumerate(CODING_SECTION_ORDER)}
CONCEPT_ORDER_MAP = {name: i for i, name in enumerate(CONCEPT_SECTION_ORDER)}


def section_rank(doc_type: str, section: str) -> int:
    if doc_type == "coding":
        return CODING_ORDER_MAP.get(section, 10_000)
    if doc_type == "concept":
        return CONCEPT_ORDER_MAP.get(section, 10_000)
    return 10_000


def load_schema_hint() -> str:
    if OUTPUT_SCHEMA_PATH.exists():
        return OUTPUT_SCHEMA_PATH.read_text(encoding="utf-8", errors="ignore").strip()
    return ""


def format_context_item(meta: Dict, text: str) -> str:
    return (
        f"[Document: {meta.get('doc_id')} | Type: {meta.get('doc_type')} | "
        f"Section: {meta.get('section')} | Source: {meta.get('source_path')}]\n"
        f"{text.strip()}"
    )


def extract_section_text(retrieved: List[Tuple[Dict, str]]) -> Dict[str, str]:
    """
    Build a mapping section -> best chunk text (first occurrence in preferred order after sorting).
    If multiple chunks share same section, keep the first one.
    """
    out: Dict[str, str] = {}
    for meta, text in retrieved:
        sec = meta.get("section", "Unknown")
        if sec not in out:
            out[sec] = text
    return out


def build_answer_coding(question: str, section_text: Dict[str, str]) -> str:
    # Minimal template-based assembly using retrieved chunks.
    quick_idea = section_text.get("Key Idea", "").strip()
    approach = section_text.get("Step-by-Step Approach", "").strip()
    code = section_text.get("Python Template", "").strip()
    complexity = section_text.get("Complexity", "").strip()
    pitfalls = section_text.get("Common Mistakes", "").strip()
    edge = section_text.get("Edge Cases", "").strip()
    self_check = section_text.get("Self-Check Examples", "").strip()
    follow = section_text.get("Follow-Up", "").strip()

    # Fallbacks if missing
    if not quick_idea:
        quick_idea = "(Not found in retrieved context) Add a 'Key Idea' section to the knowledge base."
    if not approach:
        approach = "(Not found in retrieved context) Add a 'Step-by-Step Approach' section to the knowledge base."
    if not code:
        code = "(Not found in retrieved context) Add a 'Python Template' section to the knowledge base."
    if not complexity:
        complexity = "(Not found in retrieved context) Add a 'Complexity' section to the knowledge base."
    if not pitfalls and edge:
        pitfalls = edge  # acceptable substitute in MVP
    if not pitfalls:
        pitfalls = "(Not found in retrieved context) Add 'Common Mistakes' or 'Edge Cases'."
    if not self_check:
        self_check = "(Optional) Add 'Self-Check Examples' to improve practice quality."
    if not follow:
        follow = "(Optional) Add a follow-up/variant question."

    # Ensure code block formatting if the chunk already contains code fences; otherwise wrap if it looks like python.
    code_block = code
    if "```" not in code_block and ("def " in code_block or "class " in code_block):
        code_block = "```python\n" + code_block.strip() + "\n```"

    answer = []
    answer.append("### Result Snapshot")
    answer.append(f"Question: {question.strip()}")
    answer.append("")
    answer.append("### Quick Idea")
    answer.append(quick_idea)
    answer.append("")
    answer.append("### Approach")
    answer.append(approach)
    answer.append("")
    answer.append("### Python Code")
    answer.append(code_block)
    answer.append("")
    answer.append("### Complexity")
    answer.append(complexity)
    answer.append("")
    answer.append("### Pitfalls")
    answer.append(pitfalls)
    answer.append("")
    answer.append("### Self-check")
    answer.append(self_check)
    answer.append("")
    answer.append("### Follow-up")
    answer.append(follow)
    return "\n".join(answer)


def build_answer_concept(question: str, section_text: Dict[str, str]) -> str:
    snapshot = section_text.get("Result Snapshot", "").strip()
    definition = section_text.get("Definition", "").strip()
    intuition = section_text.get("Intuition", "").strip()
    mechanism = section_text.get("Mechanism", "").strip()
    example = section_text.get("Example", "").strip()
    complexity = section_text.get("Complexity", "").strip()
    advantages = section_text.get("Advantages", "").strip()
    limitations = section_text.get("Limitations", "").strip()
    misconceptions = section_text.get("Common Misconceptions", "").strip()
    follow = section_text.get("Follow-Up Questions", "").strip()

    if not snapshot:
        snapshot = "(Not found in retrieved context) Add a 'Result Snapshot' section."
    if not definition:
        definition = "(Not found in retrieved context) Add a 'Definition' section."
    if not intuition:
        intuition = "(Optional) Add an 'Intuition' section."
    if not mechanism:
        mechanism = "(Not found in retrieved context) Add a 'Mechanism' section."
    if not limitations:
        limitations = "(Optional) Add a 'Limitations' section."
    if not misconceptions:
        misconceptions = "(Optional) Add 'Common Misconceptions'."
    if not follow:
        follow = "(Optional) Add follow-up questions."

    answer = []
    answer.append("### Result Snapshot")
    answer.append(snapshot)
    answer.append("")
    answer.append("### Definition")
    answer.append(definition)
    answer.append("")
    answer.append("### Intuition")
    answer.append(intuition)
    answer.append("")
    answer.append("### Mechanism")
    answer.append(mechanism)
    answer.append("")
    answer.append("### Example")
    answer.append(example if example else "(Optional) Add an example.")
    answer.append("")
    answer.append("### Trade-offs")
    # Use advantages/limitations as a simple trade-off bucket in MVP
    trade = []
    if advantages:
        trade.append("**Pros**\n" + advantages)
    if limitations:
        trade.append("**Cons / Limitations**\n" + limitations)
    answer.append("\n\n".join(trade) if trade else "(Optional) Add pros/cons.")
    answer.append("")
    answer.append("### Common Misconceptions")
    answer.append(misconceptions)
    answer.append("")
    answer.append("### Complexity")
    answer.append(complexity if complexity else "(Optional) Add complexity info.")
    answer.append("")
    answer.append("### Follow-up")
    answer.append(follow)
    return "\n".join(answer)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", required=True, help="User question")
    parser.add_argument("--type", default="coding", choices=["coding", "concept"], help="doc_type filter")
    parser.add_argument("--k", type=int, default=4, help="top-k retrieval")
    parser.add_argument("--show_context", action="store_true", help="Print retrieved context before answer")
    args = parser.parse_args()

    # Load schema hint (not used programmatically, but good for debugging / future LLM)
    _schema = load_schema_hint()

    # Load embed model
    model = SentenceTransformer(EMBED_MODEL_NAME)

    # Load Chroma
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR),
        settings=Settings(anonymized_telemetry=False),
    )
    collection = client.get_collection(COLLECTION_NAME)

    q_emb = model.encode([args.q], normalize_embeddings=True)[0].tolist()

    results = collection.query(
        query_embeddings=[q_emb],
        n_results=args.k,
        where={"doc_type": args.type},
        include=["documents", "metadatas", "distances"],
    )

    ids = results["ids"][0]
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    dists = results["distances"][0]

    # Deduplicate by id, then sort by preferred section order
    seen_ids = set()
    retrieved: List[Tuple[Dict, str, float, str]] = []
    for cid, doc, meta, dist in zip(ids, docs, metas, dists):
        if cid in seen_ids:
            continue
        seen_ids.add(cid)
        retrieved.append((meta, doc, dist, cid))

    # Sort by section rank first, then by distance (more similar earlier)
    retrieved.sort(key=lambda x: (section_rank(args.type, x[0].get("section", "")), x[2]))

    # Build a simplified list for section extraction
    retrieved_simple = [(meta, doc) for meta, doc, _, _ in retrieved]

    if args.show_context:
        print("\n=== Retrieved Context (sorted) ===\n")
        for meta, doc, dist, cid in retrieved:
            print(f"[id={cid} | distance={dist:.4f}]")
            print(format_context_item(meta, doc))
            print("\n---\n")

    section_text = extract_section_text(retrieved_simple)

    print("\n=== Final Answer (Template-based, No LLM) ===\n")
    if args.type == "coding":
        print(build_answer_coding(args.q, section_text))
    else:
        print(build_answer_concept(args.q, section_text))


if __name__ == "__main__":
    main()