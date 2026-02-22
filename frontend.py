import streamlit as st
import requests

st.set_page_config(page_title="Lumina Health", page_icon="🌿")
st.title("🌿 Lumina Health AI Coach")

with st.sidebar:
    st.header("User Profile")
    age = st.number_input("Age", 18, 100, 25)
    gender = st.selectbox("Gender", ["Male", "Female"])
    height = st.number_input("Height (cm)", 100, 250, 170)
    weight = st.number_input("Weight (kg)", 30, 200, 70)
    bmi = round(weight / ((height/100)**2), 2)
    st.write(f"**Calculated BMI:** {bmi}")

st.subheader("Daily Habits & Vitals")
col1, col2 = st.columns(2)
with col1:
    steps = st.number_input("Daily Steps", 0, 30000, 5000)
    bp = st.text_input("Blood Pressure", "120/80")
    exercise = st.number_input("Exercise (hrs/week)", 0.0, 20.0, 2.0)
with col2:
    sleep = st.number_input("Sleep (hrs)", 0.0, 12.0, 7.0)
    hr = st.number_input("Heart Rate", 40, 150, 72)
    alcohol = st.number_input("Alcohol (units/week)", 0, 50, 0)

smoker = st.radio("Do you smoke?", ["No", "Yes"])
diabetic = st.radio("Diabetic?", ["No", "Yes"])
heart_d = st.radio("Heart Disease?", ["No", "Yes"])

if st.button("Analyze My Lifestyle"):
    payload = {
        "Age": age, "Gender": gender, "Height_cm": height, "Weight_kg": weight, "BMI": bmi,
        "Daily_Steps": steps, "Calories_Intake": 2000, "Hours_of_Sleep": sleep,
        "Heart_Rate": hr, "Blood_Pressure": bp, "Exercise_Hours_per_Week": exercise,
        "Smoker": smoker, "Alcohol_Consumption_per_Week": alcohol,
        "Diabetic": diabetic, "Heart_Disease": heart_d
    }
    
    with st.spinner("Our AI is analyzing..."):
        res = requests.post("http://127.0.0.1:8000/analyze", json=payload).json()
        
    st.success(f"ML Status: **{res['status']}**")
    st.markdown("### 📋 Personalized Guide")
    st.write(res['recommendations'])