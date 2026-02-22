import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_ai_guide(user_data, status):
    # This prompt forces a specific Markdown structure
    prompt = f"""
    You are the HealthArc AI Coach. Analyze the following health profile and provide a structured plan.
    
    USER PROFILE:
    - Status: {status}
    - Age/Gender: {user_data['Age']} / {user_data['Gender']}
    - Vitals: BP {user_data['Blood_Pressure']}, HR {user_data['Heart_Rate']}, BMI {user_data['BMI']}
    - Habits: {user_data['Daily_Steps']} steps/day, {user_data['Exercise_Hours_per_Week']} hrs exercise/week
    
    RESPONSE REQUIREMENTS:
    1. Use Markdown headers (##) for sections.
    2. Provide exactly 3 bulleted tips.
    3. Include a 1-sentence "Weekly Challenge".
    4. Do not include any introductory fluff (e.g., "Here is your plan").
    5. Keep it professional and encouraging.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    
    return response.text