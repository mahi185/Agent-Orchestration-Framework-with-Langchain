# =====================================================
# SHARED VECTOR MEMORY USING VectorStoreRetrieverMemory
# =====================================================

import numpy as np
from langchain_classic.memory.vectorstore import VectorStoreRetrieverMemory
from langchain_community.vectorstores import FAISS
from langchain_classic.embeddings.base import Embeddings
from langchain_classic.schema import Document


# -------- SIMPLE LOCAL EMBEDDINGS (NO API) --------
class SimpleEmbeddings(Embeddings):
    def embed_documents(self, texts):
        return [self._embed(t) for t in texts]

    def embed_query(self, text):
        return self._embed(text)

    def _embed(self, text):
        vector = np.zeros(10)
        for i, char in enumerate(text[:10]):
            vector[i] = ord(char) % 100
        return vector.tolist()


# -------- SHARED VECTOR MEMORY --------
class SharedVectorMemory:
    def __init__(self):
        self.embeddings = SimpleEmbeddings()

        # initialize vectorstore with one initial document
        self.vectorstore = FAISS.from_documents(
            [Document(page_content="Initial memory")],
            self.embeddings
        )

        self.memory = VectorStoreRetrieverMemory(
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            memory_key="shared_memory"
        )

    def add(self, text):
        self.vectorstore.add_documents([Document(page_content=text)])
        print(f"Memory Added: {text}")

    def get(self, query):
        result = self.memory.load_memory_variables({"prompt": query})
        return result.get("shared_memory", "")


# -------- AGENTS --------
class PlannerAgent:
    def run(self, task, memory):
        past = memory.get(task)
        plan = f"Planning task: {task}"

        if past:
            plan += f"\nUsing past memory:\n{past}"

        memory.add(plan)
        print("\n Planner Output:\n", plan)


class ResearchAgent:
    def run(self, memory):
        research = "Research: Shared memory improves coordination between agents."
        memory.add(research)
        print("\n Research Output:\n", research)


class SummarizerAgent:
    def run(self, memory):
        summary = "Summary: Agents read and write shared vector memory."
        memory.add(summary)
        print("\n Final Summary:\n", summary)


# -------- ORCHESTRATOR --------
class AgentOrchestrator:
    def __init__(self):
        self.memory = SharedVectorMemory()
        self.planner = PlannerAgent()
        self.researcher = ResearchAgent()
        self.summarizer = SummarizerAgent()

    def run(self, task):
        print("\n STARTING AGENT ORCHESTRATION")
        self.planner.run(task, self.memory)
        self.researcher.run(self.memory)
        self.summarizer.run(self.memory)


# -------- MAIN --------
if __name__ == "__main__":
    orchestrator = AgentOrchestrator()

    orchestrator.run("Explain shared memory in multi-agent systems")

    print("\n" + "=" * 60)

    # Running twice to show how memory affects output
    orchestrator.run("Explain shared memory in multi-agent systems")
