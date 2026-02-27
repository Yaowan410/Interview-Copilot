from typing import Dict, List, Tuple, Literal
from pathlib import Path

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHROMA_DIR = PROJECT_ROOT / "chroma_db"
COLLECTION_NAME = "interview_copilot"
EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

DocType = Literal["coding", "concept"]


CODING_SECTION_ORDER = [
    "Key Idea", "Step-by-Step Approach", "Python Template", "Complexity",
    "Edge Cases", "Common Mistakes", "Self-Check Examples", "Follow-Up",
    "Pattern", "Problem Summary",
]
CONCEPT_SECTION_ORDER = [
    "Result Snapshot", "Definition", "Intuition", "Mechanism", "Example",
    "Trade-offs", "Advantages", "Limitations", "Common Misconceptions",
    "Complexity", "Follow-Up Questions",
]

CODING_ORDER_MAP = {name: i for i, name in enumerate(CODING_SECTION_ORDER)}
CONCEPT_ORDER_MAP = {name: i for i, name in enumerate(CONCEPT_SECTION_ORDER)}


def section_rank(doc_type: str, section: str) -> int:
    if doc_type == "coding":
        return CODING_ORDER_MAP.get(section, 10_000)
    if doc_type == "concept":
        return CONCEPT_ORDER_MAP.get(section, 10_000)
    return 10_000


def format_context_item(meta: Dict, text: str) -> str:
    return (
        f"[Document: {meta.get('doc_id')} | Type: {meta.get('doc_type')} | "
        f"Section: {meta.get('section')} | Source: {meta.get('source_path')}]\n"
        f"{text.strip()}"
    )


class Retriever:
    def __init__(self):
        self.embed_model = SentenceTransformer(EMBED_MODEL_NAME)
        self.client = chromadb.PersistentClient(
            path=str(CHROMA_DIR),
            settings=Settings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_collection(COLLECTION_NAME)

    def retrieve(self, question: str, doc_type: DocType, k: int = 6) -> Tuple[str, float]:
        """
        Returns:
          - formatted_context: str
          - top1_distance: float (smaller = more similar)
        """
        q_emb = self.embed_model.encode([question], normalize_embeddings=True)[0].tolist()
        results = self.collection.query(
            query_embeddings=[q_emb],
            n_results=k,
            where={"doc_type": doc_type},
            include=["documents", "metadatas", "distances"],
        )

        ids = results["ids"][0]
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        dists = results["distances"][0]

        if not ids:
            return "", 1.0

        top1_distance = float(dists[0])

        # Dedup + sort by section preference then distance
        seen = set()
        retrieved: List[Tuple[Dict, str, float]] = []
        for cid, doc, meta, dist in zip(ids, docs, metas, dists):
            if cid in seen:
                continue
            seen.add(cid)
            retrieved.append((meta, doc, float(dist)))

        retrieved.sort(key=lambda x: (section_rank(doc_type, x[0].get("section", "")), x[2]))

        context_blocks = [format_context_item(meta, doc) for meta, doc, _ in retrieved]
        return "\n\n---\n\n".join(context_blocks), top1_distance