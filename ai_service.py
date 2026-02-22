import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_ai_guide(user_data, status):
    # We use a very strict instruction set here
    prompt = f"""
    SYSTEM: You are the HealthArc AI Coach. You never mention "Lumina Health". 
    You only provide 3 health tips. No intro, no summary, no "important considerations" at the end.

    CONTEXT: 
    User is {status}. BMI: {user_data['BMI']}, Smoker: {user_data['Smoker']}, Diabetic: {user_data['Diabetic']}.

    TASK:
    Provide 3 tips. Use the EXACT format below for each tip:
    
    TITLE: [Short Catchy Title]
    DETAIL: [2-3 sentences of specific, actionable advice. Do not mention other apps.]
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text