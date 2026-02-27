import argparse
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from pathlib import Path
from typing import Dict, List, Tuple

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from openai import OpenAI


# -------- Paths / Settings --------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHROMA_DIR = PROJECT_ROOT / "chroma_db"
COLLECTION_NAME = "interview_copilot"
EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

OUTPUT_SCHEMA_PATH = PROJECT_ROOT / "docs" / "output_schema.md"

# Pick a model you have access to
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")


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


def load_output_schema() -> str:
    if OUTPUT_SCHEMA_PATH.exists():
        return OUTPUT_SCHEMA_PATH.read_text(encoding="utf-8", errors="ignore").strip()
    return ""


def format_context_item(meta: Dict, text: str) -> str:
    return (
        f"[Document: {meta.get('doc_id')} | Type: {meta.get('doc_type')} | "
        f"Section: {meta.get('section')} | Source: {meta.get('source_path')}]\n"
        f"{text.strip()}"
    )


def build_prompt(doc_type: str, schema: str, context: str, question: str) -> Tuple[str, str]:
    system = (
    "You are an Interview Practice Tutor.\n"
    "You must follow the required output schema EXACTLY.\n"
    "IMPORTANT OUTPUT RULES:\n"
    "1) Output ONLY the final answer. Do NOT repeat the schema text. Do NOT print 'Retrieved Context'.\n"
    "2) Use Markdown headings EXACTLY as written in the schema, including the leading ###.\n"
    "   For example, you MUST output headings like: '### Result Snapshot', '### Quick Idea', etc.\n"
    "3) For coding questions, include a runnable Python solution inside a ```python code block.\n"
    "4) If a section is missing from context, write a brief note in that section and continue.\n"
    )

    user = (
    f"Follow the output schema below.\n\n"
    f"{schema}\n\n"
    f"Retrieved Context:\n{context}\n\n"
    f"User Question:\n{question}\n"
    )
    return system, user


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", required=True, help="User question")
    parser.add_argument("--type", default="coding", choices=["coding", "concept"], help="doc_type filter")
    parser.add_argument("--k", type=int, default=6, help="top-k retrieval")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenAI model name")
    parser.add_argument("--show_context", action="store_true", help="Print retrieved context before final answer")
    args = parser.parse_args()

    # ---- Load schema ----
    schema = load_output_schema()
    if not schema:
        raise FileNotFoundError("docs/output_schema.md not found or empty.")

    # ---- Embedding model ----
    embed_model = SentenceTransformer(EMBED_MODEL_NAME)

    # ---- Vector DB ----
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR),
        settings=Settings(anonymized_telemetry=False),
    )
    collection = client.get_collection(COLLECTION_NAME)

    q_emb = embed_model.encode([args.q], normalize_embeddings=True)[0].tolist()

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

    # ---- Dedup + sort by preferred section order then distance ----
    seen = set()
    retrieved: List[Tuple[Dict, str, float, str]] = []
    for cid, doc, meta, dist in zip(ids, docs, metas, dists):
        if cid in seen:
            continue
        seen.add(cid)
        retrieved.append((meta, doc, dist, cid))

    retrieved.sort(key=lambda x: (section_rank(args.type, x[0].get("section", "")), x[2]))

    # ---- Format context ----
    context_blocks = []
    for meta, doc, dist, cid in retrieved:
        context_blocks.append(format_context_item(meta, doc))
    context = "\n\n---\n\n".join(context_blocks)

    if args.show_context:
        print("\n=== Retrieved Context (sorted) ===\n")
        print(context)
        print("\n===============================\n")

    # ---- Build prompt ----
    system, user = build_prompt(args.type, schema, context, args.q)

    # ---- Call OpenAI Responses API ----
    # Model is selected on responses.create. :contentReference[oaicite:1]{index=1}
    oai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError("OPENAI_API_KEY is not set. Please export it first.")

    resp = oai.responses.create(
        model=args.model,
        input=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )

    # The SDK provides output text; using output_text is the simplest.
    print(resp.output_text)


if __name__ == "__main__":
    main()