from chatbot import RAGBot

def main():
    print("== RAG Assignment Bot (Ollama + LLaMA 2) ==")
    print("Ask questions about the Transformer / BERT / GPT papers.")
    print("Type 'exit' to quit.\n")

    bot = RAGBot()

    while True:
        user = input("You: ").strip()
        if user.lower() in ["exit", "quit"]:
            break

        response = bot.ask(user)
        print("\nBot:", response, "\n")

if __name__ == "__main__":
    main()
