import argparse
from pathlib import Path

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHROMA_DIR = PROJECT_ROOT / "chroma_db"
COLLECTION_NAME = "interview_copilot"
EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", required=True, help="User question / query text")
    parser.add_argument("--type", default="coding", choices=["coding", "concept", "system", "behavioral"], help="doc_type filter")
    parser.add_argument("--k", type=int, default=4, help="top-k")
    args = parser.parse_args()

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

    print("\n=== Retrieval Results ===")
    for rank, (cid, doc, meta, dist) in enumerate(zip(ids, docs, metas, dists), start=1):
        print(f"\n--- #{rank}  id={cid}  distance={dist:.4f} ---")
        print(f"meta: doc_id={meta.get('doc_id')} | doc_type={meta.get('doc_type')} | section={meta.get('section')} | source={meta.get('source_path')}")
        print("text:")
        print(doc[:800] + ("..." if len(doc) > 800 else ""))


if __name__ == "__main__":
    main()