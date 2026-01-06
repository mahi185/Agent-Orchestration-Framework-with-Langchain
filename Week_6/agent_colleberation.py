# ================= LOAD ENV =================
from dotenv import load_dotenv
import os

load_dotenv()
print("API KEY LOADED")


# ================= LLM =================
from langchain_google_genai import ChatGoogleGenerativeAI


# ================= SHARED TEXT MEMORY =================

class SharedTextMemory:
    def __init__(self):
        self.memory = []

    def add(self, text: str):
        self.memory.append(text)

    def get_all(self):
        return "\n".join(self.memory)


# ================= BASE AGENT =================

class BaseAgent:
    def __init__(self, name, memory):
        self.name = name
        self.memory = memory
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3
        )

    def remember(self, text):
        self.memory.add(f"[{self.name}] {text}")


# ================= PLANNER AGENT =================

class PlannerAgent(BaseAgent):
    def plan(self, query):
        response = self.llm.invoke(
            f"Create a step-by-step plan for: {query}"
        ).content

        print("\n PLANNER OUTPUT:\n", response)
        self.remember(response)
        return response


# ================= RESEARCH AGENT =================

class ResearchAgent(BaseAgent):
    def research(self, task):
        response = self.llm.invoke(
            f"Research and explain clearly: {task}"
        ).content

        print("\n RESEARCH OUTPUT:\n", response)
        self.remember(response)


# ================= SUMMARIZER AGENT =================

class SummarizerAgent(BaseAgent):
    def summarize(self, query):
        context = self.memory.get_all()

        response = self.llm.invoke(
            f"Using the following shared memory:\n{context}\n\nAnswer: {query}"
        ).content

        print("\n FINAL ANSWER:\n", response)
        return response


# ================= ORCHESTRATOR =================

class AgentOrchestrator:
    def __init__(self):
        self.memory = SharedTextMemory()
        self.planner = PlannerAgent("Planner", self.memory)
        self.researcher = ResearchAgent("Researcher", self.memory)
        self.summarizer = SummarizerAgent("Summarizer", self.memory)

    def run(self, query):
        plan = self.planner.plan(query)
        self.researcher.research(plan)
        return self.summarizer.summarize(query)


# ================= RUN =================

if __name__ == "__main__":
    orchestrator = AgentOrchestrator()

    user_query = "Explain shared memory in multi-agent systems"

    print("\n STARTING MULTI-AGENT ORCHESTRATION...\n")
    orchestrator.run(user_query)

    print("\n DONE")
