from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from dotenv import load_dotenv
import os

load_dotenv()

# Use Gemini instead of ChatOpenAI
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# Dummy tool example
def greet(name: str):
    return f"Hello {name}, welcome to Agents!"

greet_tool = Tool(
    name="greeting_tool",
    func=greet,
    description="Use this to greet a person by name."
)

# Create a Zero-Shot ReAct Agent
agent = initialize_agent(
    tools=[greet_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Run agent
result = agent.run("Greet Saadhana in a friendly way.")
print(result)
