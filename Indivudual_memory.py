import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Simple memory class (like ConversationBufferMemory)
class SimpleConversationMemory:
    def __init__(self):
        self.messages = []  # list of dicts with role and content

    def add_user_message(self, text: str):
        self.messages.append({"role": "user", "content": text})

    def add_ai_message(self, text: str):
        self.messages.append({"role": "assistant", "content": text})

    def load_memory(self):
        return self.messages.copy()

# Agent class with individual memory
class Agent:
    def __init__(self, role: str):
        self.role = role
        self.memory = SimpleConversationMemory()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3
        )

    def run(self, instruction: str) -> str:
        # Add user message
        self.memory.add_user_message(instruction)

        # Load memory and prepare messages for LLM
        messages = [
            {"role": m["role"], "content": m["content"]}
            for m in self.memory.load_memory()
        ]
        response = self.llm.invoke(messages)

        # Add AI response
        self.memory.add_ai_message(response.content)
        return response.content

# Multi-agent system
if __name__ == "__main__":
    research_agent = Agent("Research Agent")
    summary_agent = Agent("Summary Agent")

    print("Multi-Agent System with Individual Memory (Gemini API)\n")

    while True:
        user_input = input("Enter your question: ")
        if user_input.lower() == "exit":
            break

        print("\n---- Research Agent ----")
        research_output = research_agent.run(user_input)
        print(research_output)

        print("\n---- Summary Agent ----")
        summary_output = summary_agent.run(
            f"Summarize the following in 3 points:\n{research_output}"
        )
        print(summary_output)

        print("\n" + "-" * 60 + "\n")

