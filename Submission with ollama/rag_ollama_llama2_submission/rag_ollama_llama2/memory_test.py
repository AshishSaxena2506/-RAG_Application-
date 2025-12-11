# memory_test.py
"""
Task 4 – Conversational memory smoke test.

This does NOT change the chatbot's behaviour. It simply imports the
existing RAGBot and runs a small scripted conversation to show that
the bot remembers information across turns.
"""

from chatbot import RAGBot


def run_memory_test():
    bot = RAGBot()

    turns = [
        "My name is Ashish, remember this.",
        "What is self-attention in Transformers?",
        "And what is my name?",
    ]

    print("== TASK 4: Conversational Memory Test ==")
    print("This uses the SAME RAG bot and personality as run_chat.py.\n")

    for i, user_q in enumerate(turns, start=1):
        print(f"\n-------------------------")
        print(f"Turn {i}")
        print(f"You: {user_q}")
        answer = bot.ask(user_q)
        print("Bot:", answer)

    print("\n==============================")
    print("Task 4 finished.")
    print("Check Turn 3: the bot should answer that your name is Ashish.")
    print("==============================")

if __name__ == "__main__":
    run_memory_test()
