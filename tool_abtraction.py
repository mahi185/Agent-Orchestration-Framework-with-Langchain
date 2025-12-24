import os
from dotenv import load_dotenv

from langchain_core.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ----------------------------
# Load environment
# ----------------------------
load_dotenv(r"E:\Users\HP\Desktop\Agent-Orichestration framework with Langchain\.env")

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment!")

print("GEMINI_API_KEY loaded successfully")

# ----------------------------
# Define Summarizer Tool
# ----------------------------
def summarizer(text: str) -> str:
    """
    Simple demo summarizer: truncates text to first 100 chars
    """
    return text[:100] + "..." if len(text) > 100 else text

# Wrap as LangChain Tool
tools = [
    Tool(
        name="summarizer",
        func=summarizer,
        description="Summarize a long text into a concise summary. Example: 'summarize: <text>'."
    )
]

# ----------------------------
# Initialize Gemini LLM
# ----------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0
)

# ----------------------------
# Create Prompt + Chain
# ----------------------------
prompt = PromptTemplate(
    input_variables=["input", "tools", "tool_names"],
    template="""
You are a helpful AI assistant. You can also use tools when appropriate.

Available tools:
{tools}

Tool names: {tool_names}

Question: {input}
"""
)

chain = prompt | llm | StrOutputParser()

# ----------------------------
# Interactive Loop
# ----------------------------
if __name__ == "__main__":
    print("Gemini Chain with Summarizer Tool Ready! Type 'exit' to quit.\n")

    tool_names = [t.name for t in tools]

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        # Simple tool dispatch: check if user wants to summarize
        if user_input.lower().startswith("summarize"):
            text_to_summarize = user_input.split(":", 1)[1].strip() if ":" in user_input else user_input
            result = summarizer(text_to_summarize)
        else:
            result = chain.invoke({
                "input": user_input,
                "tools": "\n".join([f"{t.name}: {t.description}" for t in tools]),
                "tool_names": ", ".join(tool_names)
            })

        print("AI:", result)
