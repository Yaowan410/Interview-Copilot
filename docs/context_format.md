# Retrieved Context Formatting

This document defines how retrieved chunks should be formatted and passed to downstream generation (LLM or template-based).

---

## 1. Purpose

- Keep retrieval results readable and traceable.
- Preserve section labels to help structured answering.
- Allow later citation or debugging.

---

## 2. Canonical Format (per chunk)

Each retrieved chunk MUST be rendered as:
[Document: <doc_id> | Type: <doc_type> | Section: <section> | Source: <source_path>]
<chunk_text>


Example:


[Document: valid_parenthesis | Type: coding | Section: Key Idea | Source: data/algorithm/valid_parenthesis.md]
We use a stack to track opening brackets...


---

## 3. Chunk Ordering Rules (MVP)

### Coding questions preferred order
1) Key Idea
2) Step-by-Step Approach
3) Python Template
4) Complexity
5) Edge Cases
6) Common Mistakes
7) Self-Check Examples
8) Follow-Up
9) Problem Summary

### Concept questions preferred order
1) Result Snapshot
2) Definition
3) Intuition
4) Mechanism
5) Example
6) Trade-offs / Advantages / Limitations
7) Common Misconceptions
8) Complexity
9) Follow-Up Questions

If multiple chunks share the same section name, keep original retrieval order among them.

---

## 4. Deduplication (MVP)

- Deduplicate exact same chunk IDs.
- Allow multiple sections from the same document.
- Do NOT merge chunk texts (keep them separate) for traceability.

---

## 5. Notes

- In the MVP, the final answer can be template-based (no LLM).
- Later, the same formatted context can be appended into an LLM prompt.