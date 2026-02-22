import os
import joblib
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv

load_dotenv() # Create a .env file with GEMINI_API_KEY=your_key

app = FastAPI()

# Load ML Assets
model = joblib.load("lifestyle_model.joblib")
le_gender = joblib.load("gender_encoder.joblib")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class UserData(BaseModel):
    Age: int; Gender: str; Height_cm: int; Weight_kg: int; BMI: float
    Daily_Steps: int; Calories_Intake: int; Hours_of_Sleep: float
    Heart_Rate: int; Blood_Pressure: str; Exercise_Hours_per_Week: float
    Smoker: str; Alcohol_Consumption_per_Week: int
    Diabetic: str; Heart_Disease: str

@app.post("/analyze")
async def analyze(user: UserData):
    # 1. ML Prediction
    sys, dia = map(int, user.Blood_Pressure.split('/'))
    gen_enc = le_gender.transform([user.Gender])[0]
    b_map = {'No': 0, 'Yes': 1}
    
    vector = [[
        user.Age, gen_enc, user.Height_cm, user.Weight_kg, user.BMI,
        user.Daily_Steps, user.Calories_Intake, user.Hours_of_Sleep,
        user.Heart_Rate, sys, dia, user.Exercise_Hours_per_Week,
        b_map[user.Smoker], user.Alcohol_Consumption_per_Week,
        b_map[user.Diabetic], b_map[user.Heart_Disease]
    ]]
    
    status = model.predict(vector)[0]

    # 2. Gemini Guidance
    prompt = f"User is {status}. Stats: {user.dict()}. Give 3 health tips for our app Lumina Health."
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    
    return {"status": status, "recommendations": response.text}