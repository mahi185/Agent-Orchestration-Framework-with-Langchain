import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

load_dotenv()

# Connect to Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Prompt template
prompt = PromptTemplate(
    input_variables=["topic"],
    template="Explain this topic in simple words: {topic}"
)

# New way: prompt | llm
chain = prompt | llm  
# Invoke the chain
result = chain.invoke({"topic": "defination of llm"})
print(result)
