import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool

# ----------------------------
# Load environment
# ----------------------------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment!")

# ----------------------------
# Define Calculator Tool
# ----------------------------
@tool
def calculator(expression: str) -> str:
    """Calculate simple math expressions like '23+45'"""
    try:
        return str(eval(expression))
    except Exception:
        return "Invalid Math Expression"

tools = [calculator]

# ----------------------------
# Initialize Gemini LLM
# ----------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",  # use a valid model
    google_api_key="GOOGLE_API_KEY",
    temperature=0
)

# ----------------------------
# Simple agent loop
# ----------------------------
print("Gemini Calculator Agent Ready! Type 'exit' to quit.\n")

while True:
    query = input("You: ")
    if query.lower() == "exit":
        break

    # Check if the query is a math expression
    if any(op in query for op in ["+", "-", "*", "/"]):
        # Use calculator tool
        result = calculator(query)
    else:
        # Use Gemini LLM directly
        response = llm.chat(messages=[{"role": "user", "content": query}])
        result = response.content if hasattr(response, "content") else str(response)

    print("Agent:", result)
