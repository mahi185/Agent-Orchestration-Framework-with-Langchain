import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load model
model = genai.GenerativeModel("gemini-2.5-flash")

# Generate output
response = model.generate_content(
    "You are a helpful AI assistant"
)

print(response.text)