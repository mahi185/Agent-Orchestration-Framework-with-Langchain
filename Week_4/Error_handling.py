from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool   
import traceback

# -------------------------------
# Define tools using decorator
# -------------------------------
@tool
def calculator(expression: str) -> str:
    """Perform simple math calculations."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Calculation error: {e}"

@tool
def echo(text: str) -> str:
    """Repeats user input."""
    return f"You said: {text}"

tools = [calculator, echo]

# -------------------------------
# Initialize Gemini LLM
# -------------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key="GOOGLE_KEY"
)

# -------------------------------
# Function to run agent
# -------------------------------
def run_agent(query: str):
    try:
        response = llm.invoke(query)
        content = response.content

        # Very simple tool trigger (manual)
        if "calculator" in query.lower():
            return calculator.invoke(query.replace("calculator", "").strip())
        if "echo" in query.lower():
            return echo.invoke(query.replace("echo", "").strip())

        return content

    except Exception as e:
        print("API Error:", e)
        traceback.print_exc()
        return "Error processing your request."

# -------------------------------
# Interactive loop
# -------------------------------
if __name__ == "__main__":
    print("Gemini Agent ready! Type a query (or 'exit' to quit).")
    while True:
        query = input(">> ")
        if query.lower() == "exit":
            break
        result = run_agent(query)
        print("Agent:", result)
