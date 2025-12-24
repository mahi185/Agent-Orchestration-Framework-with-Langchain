import os
from dotenv import load_dotenv

from langchain_core.tools import Tool

# ------------------------
# TOOL FUNCTIONS
# ------------------------
def calculator(expression: str):
    try:
        return str(eval(expression))
    except Exception:
        return "Invalid Math Expression"

def weather(city: str):
    """
    Simple fake weather response.
    Replace with real API if needed.
    """
    sample = {
        "Kurnool": "Sunny, 32°C",
        "guntur": "Hot, 34°C",
        "hyderabad": "Cloudy, 28°C",
        "bangalore": "Rainy, 22°C",
    }
    return sample.get(city.lower(), "Weather unavailable for this city")

def summarizer(text: str):
    """
    Simple demo summarizer.
    Replace with LLM-based summarization if needed.
    """
    return text[:100] + "..." if len(text) > 100 else text

# ------------------------
# REGISTER TOOLS
# ------------------------
tools = [
    Tool(
        name="calculator",
        func=calculator,
        description="Calculate math expressions like '23+45'."
    ),
    Tool(
        name="weather",
        func=weather,
        description="Get weather of a city. Example: 'weather: hyderabad'"
    ),
    Tool(
        name="summarizer",
        func=summarizer,
        description="Summarize a long text into a concise summary. Example: 'summarize: <text>'."
    )
]

# ------------------------
# AGENT SETUP
# ------------------------
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import create_react_agent 
from langchain_core.prompts import PromptTemplate

load_dotenv()

def create_agent():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )

    # ---- REQUIRED REACT TEMPLATE ----
    prompt = PromptTemplate(
        input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
        template="""You are a helpful AI agent. Use tools when needed.

Available tools:
{tools}

Tool names: {tool_names}

Question: {input}

{agent_scratchpad}
"""
    )

    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )

    return agent_executor

# ------------------------
# INTERACTIVE LOOP
# ------------------------
if __name__ == "__main__":
    agent = create_agent()

    print("Gemini ReAct Agent Ready!")
    print("Type 'exit' to quit\n")

    while True:
        query = input("You: ")

        if query.lower() == "exit":
            break

        try:
            response = agent.invoke({"input": query})
            print("Agent:", response["output"])
        except Exception as e:
            print("Error:", e)
