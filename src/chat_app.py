import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import argparse
from typing import List, Dict

from openai import OpenAI

from src.rag.router import route_type
from src.rag.retriever import Retriever
from src.rag.prompts import (
    load_output_schema,
    build_system_prompt,
    build_user_message,
    build_other_style_hint,
)


def summarize_history(oai: OpenAI, model: str, existing_summary: str, history: List[Dict[str, str]]) -> str:
    """
    Compress conversation into durable long-term memory.
    Keep: user goal, preferences, current focus, open items.
    Remove: long code, verbose repetition.
    """
    dialogue = []
    for m in history:
        role = m["role"]
        content = m["content"]
        if len(content) > 1200:
            content = content[:1200] + "...(truncated)"
        dialogue.append(f"{role.upper()}: {content}")

    prompt = (
        "Update the long-term memory summary based on the recent dialogue.\n"
        "Rules:\n"
        "- Under 120 words.\n"
        "- Keep: goals, preferences, constraints, what is solved, open tasks.\n"
        "- Drop: long code, repeated details.\n\n"
        f"Existing long-term memory:\n{existing_summary}\n\n"
        f"Recent dialogue:\n" + "\n".join(dialogue) + "\n\n"
        "Return ONLY the updated long-term memory text."
    )

    resp = oai.responses.create(
        model=model,
        input=[
            {"role": "system", "content": "You summarize conversation into durable memory."},
            {"role": "user", "content": prompt},
        ],
    )
    return resp.output_text.strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-4o"), help="OpenAI model name")
    parser.add_argument("--k", type=int, default=6, help="top-k retrieval")
    parser.add_argument("--max_turns", type=int, default=6, help="keep last N turns (user+assistant) as short-term memory")
    parser.add_argument("--show_router", action="store_true")
    parser.add_argument("--show_context", action="store_true")
    parser.add_argument("--use_summary", action="store_true", help="enable long-term memory summary")
    parser.add_argument("--summary_every", type=int, default=6, help="refresh summary every N user turns")
    parser.add_argument("--min_relevance", type=float, default=0.60, help="if top1 distance > this, treat as insufficient context")
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError("OPENAI_API_KEY is not set. Please export it first.")

    oai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    schema = load_output_schema()

    # Two system prompts:
    # - structured: for coding/concept
    # - general: for other
    structured_system = build_system_prompt(schema)
    other_system = build_other_style_hint()

    retriever = Retriever()

    # Memory
    history: List[Dict[str, str]] = []
    summary = ""
    user_turns = 0

    print("Interview Copilot (RAG + LLM, multi-turn memory)")
    print("Type 'exit' to quit. Type 'reset' to clear memory.\n")

    try:
        while True:
            user_text = input("You: ").strip()
            if not user_text:
                continue
            if user_text.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            if user_text.lower() == "reset":
                history.clear()
                summary = ""
                user_turns = 0
                print("(memory cleared)\n")
                continue

            user_turns += 1

            doc_type = route_type(user_text)
            if args.show_router:
                print(f"[router] type={doc_type}")

            # other: no RAG
            if doc_type == "other":
                user_msg = build_user_message("other", user_text, context="", memory=summary)
                resp = oai.responses.create(
                    model=args.model,
                    input=[{"role": "system", "content": other_system}] + history + [{"role": "user", "content": user_msg}],
                )
                assistant_text = resp.output_text.strip()

                print("\nBot:\n")
                print(assistant_text)
                print("\n" + "=" * 60 + "\n")

                history.append({"role": "user", "content": user_text})
                history.append({"role": "assistant", "content": assistant_text})

            else:
                # coding / concept: retrieve context
                context, top1_dist = retriever.retrieve(user_text, doc_type=doc_type, k=args.k)
                if args.show_context:
                    print("\n=== Retrieved Context ===\n")
                    print(context)
                    print("\n========================\n")

                # If retrieval is not relevant enough, avoid hallucination:
                if not context or top1_dist > args.min_relevance:
                    assistant_text = (
                        "### Result Snapshot\n"
                        "I don’t have enough relevant context in the knowledge base to answer this reliably.\n\n"
                        "### Quick Idea\n"
                        "Add a short markdown note for this topic under `data/` (algorithm/ or concept/), then rebuild the index.\n\n"
                        "### Approach\n"
                        "1) Create a new .md file with sections like Key Idea / Step-by-Step / Python Template (if coding).\n"
                        "2) Run `python -m src.rag.build_index`.\n"
                        "3) Ask again.\n\n"
                        "### Python Code\n"
                        "(Not available — insufficient context)\n\n"
                        "### Complexity\n"
                        "(Not available)\n\n"
                        "### Pitfalls\n"
                        "(Not available)\n\n"
                        "### Self-check\n"
                        "(Not available)\n\n"
                        "### Follow-up\n"
                        "Tell me what exact topic you want added to the knowledge base."
                    )
                    print("\nBot:\n")
                    print(assistant_text)
                    print("\n" + "=" * 60 + "\n")

                    history.append({"role": "user", "content": user_text})
                    history.append({"role": "assistant", "content": assistant_text})

                else:
                    user_msg = build_user_message(doc_type, user_text, context=context, memory=summary)
                    # Add this turn to conversational memory (structured)
                    history.append({"role": "user", "content": user_msg})

                    # Keep short-term memory bounded
                    max_msgs = max(2 * args.max_turns, 2)
                    if len(history) > max_msgs:
                        history = history[-max_msgs:]

                    resp = oai.responses.create(
                        model=args.model,
                        input=[{"role": "system", "content": structured_system}] + history,
                    )
                    assistant_text = resp.output_text.strip()

                    print("\nBot:\n")
                    print(assistant_text)
                    print("\n" + "=" * 60 + "\n")

                    history.append({"role": "assistant", "content": assistant_text})
                    if len(history) > max_msgs:
                        history = history[-max_msgs:]

            # Long-term summary refresh
            if args.use_summary and (user_turns % args.summary_every == 0) and history:
                summary = summarize_history(oai, args.model, summary, history)

    except KeyboardInterrupt:
        print("\nGoodbye!")


if __name__ == "__main__":
    main()