import subprocess

def main():
    print("Interview Copilot (RAG + LLM)")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()
        if question.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        cmd = [
            "python",
            "-m",
            "src.rag.answer_with_llm",
            "--q",
            question,
            "--type",
            "coding",
            "--k",
            "6"
        ]

        print("\nBot:\n")
        subprocess.run(cmd)
        print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()