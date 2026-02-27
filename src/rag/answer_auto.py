import argparse
import subprocess
import sys

from .router import route_type


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", required=True, help="User question")
    parser.add_argument("--k", type=int, default=6, help="top-k retrieval")
    parser.add_argument("--model", default=None, help="override OpenAI model")
    parser.add_argument("--show_context", action="store_true")
    args = parser.parse_args()

    doc_type = route_type(args.q)

    cmd = [
        sys.executable,
        "-m",
        "src.rag.answer_with_llm",
        "--type",
        doc_type,
        "--q",
        args.q,
        "--k",
        str(args.k),
    ]

    if args.model:
        cmd += ["--model", args.model]
    if args.show_context:
        cmd += ["--show_context"]

    subprocess.run(cmd, check=False)


if __name__ == "__main__":
    main()