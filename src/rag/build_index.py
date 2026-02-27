import re
from pathlib import Path
from typing import List, Dict, Tuple

from tqdm import tqdm
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


# ---------- Paths ----------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
CHROMA_DIR = PROJECT_ROOT / "chroma_db"
COLLECTION_NAME = "interview_copilot"

# ---------- Embedding Model ----------
EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def infer_doc_type(path: Path) -> str:
    p = str(path).replace("\\", "/").lower()
    if "/algorithm/" in p:
        return "coding"
    if "/concept/" in p:
        return "concept"
    if "/system/" in p:
        return "system"
    if "/behavioral/" in p:
        return "behavioral"
    return "unknown"


def doc_id_from_path(path: Path) -> str:
    return path.stem.strip().lower()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def split_by_h2(md: str) -> List[Tuple[str, str]]:
    """
    Split markdown by '## ' headings.
    Returns list of (section_title, section_body).
    If no '## ' headings exist, returns one chunk with section='Full Doc'.
    """
    # Normalize line endings
    md = md.replace("\r\n", "\n").replace("\r", "\n")

    # Find all H2 headings
    matches = list(re.finditer(r"(?m)^##\s+(.*)\s*$", md))
    if not matches:
        body = md.strip()
        return [("Full Doc", body)] if body else []

    chunks = []
    for i, m in enumerate(matches):
        title = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        body = md[start:end].strip()
        if body:
            chunks.append((title, body))
    return chunks


def main():
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"DATA_DIR not found: {DATA_DIR}")

    md_files = sorted(DATA_DIR.rglob("*.md"))
    if not md_files:
        raise RuntimeError(f"No markdown files found under: {DATA_DIR}")

    print(f"[build_index] Found {len(md_files)} markdown files.")

    # Init embedding model
    model = SentenceTransformer(EMBED_MODEL_NAME)

    # Init Chroma (persistent)
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR),
        settings=Settings(anonymized_telemetry=False),
    )

    # Recreate collection each time (simple MVP)
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    ids = []
    documents = []
    metadatas = []

    for path in md_files:
        doc_type = infer_doc_type(path)
        doc_id = doc_id_from_path(path)
        md = read_text(path)

        sections = split_by_h2(md)
        for idx, (section_title, section_body) in enumerate(sections):
            chunk_id = f"{doc_id}::s{idx:02d}"

            # Store section label in the document itself to help LLM later
            chunk_text = f"[Section: {section_title}]\n{section_body}".strip()

            ids.append(chunk_id)
            documents.append(chunk_text)
            metadatas.append(
                {
                    "doc_id": doc_id,
                    "doc_type": doc_type,
                    "section": section_title,
                    "source_path": str(path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
                }
            )

    print(f"[build_index] Total chunks: {len(ids)}")

    # Embed in batches (SentenceTransformer handles batching internally)
    embeddings = model.encode(documents, show_progress_bar=True, normalize_embeddings=True)

    # Add to Chroma
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings.tolist(),
    )

    print(f"[build_index] Done. Persisted to: {CHROMA_DIR}")


if __name__ == "__main__":
    main()