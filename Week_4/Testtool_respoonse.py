# Testtool_respoonse.py

from typing import List
from langchain.agents import Tool, create_react_agent
from langchain.prompts import StringPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# 1 Define your tools
tools = [
    Tool(
        name="Calculator",
        func=lambda x: str(eval(x)),
        description="Useful for math calculations"
    ),
    Tool(
        name="Echo",
        func=lambda x: f"You said: {x}",
        description="Repeats back the user query"
    )
]

# 2 Custom prompt template with implemented format()
class CustomPromptTemplate(StringPromptTemplate):
    template: str = """You are an agent with access to these tools: {tools}.
Tool names: {tool_names}.
Answer the user input: {input}"""

    input_variables: List[str] = ["input", "tools", "tool_names"]

    def format(self, **kwargs) -> str:
        return self.template.format(**kwargs)

# 3 Initialize Gemini LLM with API key directly
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",  # or "gemini-2.5-flash", etc.
    google_api_key="YOUR_GOOGLE_API_KEY"  # <-- Replace with your actual key
)

# 4.Create the agent
prompt = CustomPromptTemplate()

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# 5.Interactive loop
if __name__ == "__main__":
    print("Gemini Agent ready! Type a query (or 'exit' to quit).")
    while True:
        query = input(">> ")
        if query.lower() == "exit":
            break
        result = agent.run(query)
        print("Agent:", result)
