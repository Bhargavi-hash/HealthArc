import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

class LifestyleModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.le_gender = LabelEncoder()
        self.binary_map = {'No': 0, 'Yes': 1}
        self.features = [
            'Age', 'Gender_Encoded', 'Height_cm', 'Weight_kg', 'BMI', 
            'Daily_Steps', 'Calories_Intake', 'Hours_of_Sleep', 'Heart_Rate', 
            'Systolic', 'Diastolic', 'Exercise_Hours_per_Week', 'Smoker', 
            'Alcohol_Consumption_per_Week', 'Diabetic', 'Heart_Disease'
        ]

    def train(self, df):
        temp_df = df.copy()
        temp_df[['Systolic', 'Diastolic']] = temp_df['Blood_Pressure'].str.split('/', expand=True).astype(int)
        temp_df['Gender_Encoded'] = self.le_gender.fit_transform(temp_df['Gender'])
        
        for col in ['Smoker', 'Diabetic', 'Heart_Disease']:
            temp_df[col] = temp_df[col].map(self.binary_map)

        def label_logic(row):
            score = 0
            if row['Daily_Steps'] > 10000: score += 1
            if row['Smoker'] == 0: score += 1
            if 18.5 <= row['BMI'] <= 24.9: score += 1
            if row['Exercise_Hours_per_Week'] >= 3: score += 1
            return 'Optimal' if score >= 3 else 'Balanced' if score == 2 else 'At Risk'

        y = temp_df.apply(label_logic, axis=1)
        X = temp_df[self.features]
        self.model.fit(X, y)

    def predict(self, data):
        sys, dia = map(int, data['Blood_Pressure'].split('/'))
        gen_enc = self.le_gender.transform([data['Gender']])[0]
        
        vector = [
            data['Age'], gen_enc, data['Height_cm'], data['Weight_kg'], data['BMI'],
            data['Daily_Steps'], data['Calories_Intake'], data['Hours_of_Sleep'],
            data['Heart_Rate'], sys, dia, data['Exercise_Hours_per_Week'],
            self.binary_map[data['Smoker']], data['Alcohol_Consumption_per_Week'],
            self.binary_map[data['Diabetic']], self.binary_map[data['Heart_Disease']]
        ]
        return self.model.predict([vector])[0]