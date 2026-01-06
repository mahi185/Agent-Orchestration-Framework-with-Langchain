import os







from dotenv import load_dotenv
from langchain_classic.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Agent class with individual memory
class Agent:
    def __init__(self, role):
        self.role = role
        self.memory = ConversationBufferMemory(return_messages=True)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3
        )

    def run(self, instruction: str) -> str:
        self.memory.chat_memory.add_user_message(instruction)
        messages = self.memory.chat_memory.messages
        response = self.llm.invoke(messages)
        self.memory.chat_memory.add_ai_message(response.content)
        return response.content

# Main multi-agent loop
if __name__ == "__main__":
    research_agent = Agent("Research Agent")
    summary_agent = Agent("Summary Agent")

    print("🔹 Multi-Agent System with Individual Memory (type 'exit' to quit)\n")
    while True:
        user_input = input("Enter your question: ")
        if user_input.lower() == "exit":
            print("Exiting system...")
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
