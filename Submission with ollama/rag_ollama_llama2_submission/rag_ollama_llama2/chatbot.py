from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from vector_store import load_vector_store

class RAGBot:
    def __init__(self):
        # LLaMA2 model
        self.llm = Ollama(model="llama2")

        # Remember last 4 turns
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            input_key="user_input",
            k=4
        )

        # Vector DB for RAG
        self.db = load_vector_store()

        # Prompt template that includes:
        # - Memory
        # - Retrieved context
        template = """
You are a helpful RAG assistant.

Conversation history:
{chat_history}

Relevant paper context:
{context}

User: {user_input}
Assistant:"""

        prompt = PromptTemplate(
            template=template,
            input_variables=["chat_history", "context", "user_input"],
        )

        self.chain = LLMChain(
            llm=self.llm,
            prompt=prompt,
            memory=self.memory,
            output_key="answer"
        )

    def ask(self, query):
        # Retrieve context from Vector DB
        docs = self.db.similarity_search(query, k=3)
        context = "\n\n".join([d.page_content for d in docs])

        # Run the chain (produces and stores memory)
        return self.chain.invoke({
            "user_input": query,
            "context": context
        })["answer"]
