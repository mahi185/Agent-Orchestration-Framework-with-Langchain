# ============================================
# MULTI-AGENT ORCHESTRATION WITH SHARED MEMORY
# Single-file implementation
# ============================================

# -------- SHARED MEMORY --------
class SharedMemory:
    def __init__(self):
        self.memory = {}

    def write(self, key, value):
        print(f"Memory Updated: {key}")
        self.memory[key] = value

    def read(self, key):
        return self.memory.get(key)

    def read_all(self):
        return self.memory


# -------- PLANNER AGENT --------
class PlannerAgent:
    def run(self, task, memory):
        print("\n PLANNER AGENT RUNNING...")

        existing_plan = memory.read("plan")

        if existing_plan:
            plan = f"Refined Plan based on previous memory:\n{existing_plan}"
        else:
            plan = f"Step 1: Understand task\nStep 2: Research\nStep 3: Summarize\nTask: {task}"

        memory.write("plan", plan)
        print("Planner Output:\n", plan)


# -------- RESEARCH AGENT --------
class ResearchAgent:
    def run(self, memory):
        print("\n RESEARCH AGENT RUNNING...")

        plan = memory.read("plan")

        research = f"Research completed following plan:\n{plan}\nKey Insight: Shared memory enables coordination."

        memory.write("research", research)
        print("Research Output:\n", research)


# -------- SUMMARIZER AGENT --------
class SummarizerAgent:
    def run(self, memory):
        print("\n SUMMARIZER AGENT RUNNING...")

        research = memory.read("research")

        summary = (
            "FINAL SUMMARY:\n"
            "Agents collaborated using shared memory.\n"
            "Each agent read previous data and updated memory.\n"
            "This ensured future decisions were informed.\n\n"
            f"Based on Research:\n{research}"
        )

        memory.write("final_output", summary)
        print(" Final Output:\n", summary)


# -------- ORCHESTRATOR --------
class AgentOrchestrator:
    def __init__(self):
        self.memory = SharedMemory()
        self.planner = PlannerAgent()
        self.researcher = ResearchAgent()
        self.summarizer = SummarizerAgent()

    def run(self, task):
        print("\n STARTING MULTI-AGENT ORCHESTRATION...")
        self.planner.run(task, self.memory)
        self.researcher.run(self.memory)
        self.summarizer.run(self.memory)

        return self.memory.read("final_output")


# -------- MAIN EXECUTION --------
if __name__ == "__main__":
    orchestrator = AgentOrchestrator()

    # First run
    output1 = orchestrator.run("Explain shared memory in multi-agent systems")

    print("\n" + "=" * 60)

    # Second run (shows memory-guided decision making)
    output2 = orchestrator.run("Explain shared memory in multi-agent systems")
