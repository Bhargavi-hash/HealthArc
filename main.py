from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from ml_logic import LifestyleModel
from ai_service import get_ai_guide

app = FastAPI(title="HealthArc API")
ml_engine = LifestyleModel()

# In a real app, you'd load your CSV here
# health_df = pd.read_csv("health_data.csv")
# ml_engine.train(health_df)

class UserData(BaseModel):
    Age: int
    Gender: str
    Height_cm: int
    Weight_kg: int
    BMI: float
    Daily_Steps: int
    Calories_Intake: int
    Hours_of_Sleep: float
    Heart_Rate: int
    Blood_Pressure: str
    Exercise_Hours_per_Week: float
    Smoker: str
    Alcohol_Consumption_per_Week: int
    Diabetic: str
    Heart_Disease: str

@app.post("/analyze")
async def analyze_health(user: UserData):
    data_dict = user.dict()
    status = ml_engine.predict(data_dict)
    advice = get_ai_guide(data_dict, status)
    
    return {
        "lifestyle_status": status,
        "ai_recommendations": advice
    }