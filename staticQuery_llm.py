from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()

# Create the model
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Simple function acting like an agent
def ask_agent(question):
    result = model.invoke(question)
    return result.content

# Test your agent
print(ask_agent("What is the capital of india?"))