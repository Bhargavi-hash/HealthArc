import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_ai_guide(user_data, status):
    prompt = f"Act as a health coach. User is categorized as {status}. Data: {user_data}. Give 3 tips."
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text