import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GEMINI_API_KEY not found in .env file")

# --------------------------------------------------
# Shared Memory for all agents
# --------------------------------------------------
class SharedMemory:
    def __init__(self):
        self.messages = []

    def add_user(self, text):
        self.messages.append(HumanMessage(content=text))

    def add_ai(self, text):
        self.messages.append(AIMessage(content=text))

    def get(self):
        return self.messages

# --------------------------------------------------
# Agent Class
# --------------------------------------------------
class Agent:
    def __init__(self, role, shared_memory):
        self.role = role
        self.memory = shared_memory
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3
        )

    def run(self, instruction):
        self.memory.add_user(f"[{self.role}] Instruction: {instruction}")
        response = self.llm.invoke(self.memory.get())
        self.memory.add_ai(f"[{self.role}] {response.content}")
        return response.content

# --------------------------------------------------
# Multi-Agent System with Communication
# --------------------------------------------------
if __name__ == "__main__":
    shared_memory = SharedMemory()
    
    research_agent = Agent("Research Agent", shared_memory)
    summary_agent = Agent("Summary Agent", shared_memory)

    print("🔹 Multi-Agent System with Shared Memory (type 'exit' to quit)\n")

    while True:
        user_input = input("Enter your question: ")

        if user_input.lower() == "exit":
            print("Exiting system...")
            break

        # Step 1: Research Agent generates info
        print("\n---- Research Agent ----")
        research_output = research_agent.run(user_input)
        print(research_output)

        # Step 2: Summary Agent reads the shared memory & summarizes
        print("\n---- Summary Agent ----")
        summary_output = summary_agent.run(f"Summarize the latest research above in 3 points")
        print(summary_output)

        print("\n" + "-" * 60 + "\n")
