import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# 1. Load Data
df = pd.read_csv("health_data.csv") 

# 2. Preprocess
df[['Systolic', 'Diastolic']] = df['Blood_Pressure'].str.split('/', expand=True).astype(int)
le_gender = LabelEncoder()
df['Gender_Encoded'] = le_gender.fit_transform(df['Gender'])

binary_map = {'No': 0, 'Yes': 1}
for col in ['Smoker', 'Diabetic', 'Heart_Disease']:
    df[col] = df[col].map(binary_map)

def label_logic(row):
    score = 0
    if row['Daily_Steps'] > 10000: score += 1
    if row['Smoker'] == 0: score += 1
    if 18.5 <= row['BMI'] <= 24.9: score += 1
    if row['Exercise_Hours_per_Week'] >= 3: score += 1
    return 'Optimal' if score >= 3 else 'Balanced' if score == 2 else 'At Risk'

y = df.apply(label_logic, axis=1)
features = ['Age', 'Gender_Encoded', 'Height_cm', 'Weight_kg', 'BMI', 
            'Daily_Steps', 'Calories_Intake', 'Hours_of_Sleep', 'Heart_Rate', 
            'Systolic', 'Diastolic', 'Exercise_Hours_per_Week', 'Smoker', 
            'Alcohol_Consumption_per_Week', 'Diabetic', 'Heart_Disease']
X = df[features]

# 3. Train & Save
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

joblib.dump(model, "lifestyle_model.joblib")
joblib.dump(le_gender, "gender_encoder.joblib")
print("✅ Assets saved: lifestyle_model.joblib, gender_encoder.joblib")