import streamlit as st
import requests

st.set_page_config(page_title="HealthArc", page_icon="🌿")
st.title("🌿 HealthArc AI Coach")

# --- SIDEBAR: USER PROFILE ---
with st.sidebar:
    st.header("User Profile")
    age = st.number_input("Age", 18, 100, 25)
    gender = st.selectbox("Gender", ["Male", "Female"])
    height = st.number_input("Height (cm)", 100, 250, 170)
    weight = st.number_input("Weight (kg)", 30, 200, 70)
    bmi = round(weight / ((height/100)**2), 2)
    st.write(f"**Calculated BMI:** {bmi}")

# --- MAIN PAGE: HABITS & VITALS ---
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

# --- NEW: SIDE-BY-SIDE RADIO BUTTONS ---
st.markdown("---")
r_col1, r_col2, r_col3 = st.columns(3)
with r_col1:
    smoker = st.radio("Smoker?", ["No", "Yes"])
with r_col2:
    diabetic = st.radio("Diabetic?", ["No", "Yes"])
with r_col3:
    heart_d = st.radio("Heart Issue?", ["No", "Yes"])

if st.button("Analyze My Lifestyle", use_container_width=True):
    payload = {
        "Age": age, "Gender": gender, "Height_cm": height, "Weight_kg": weight, "BMI": bmi,
        "Daily_Steps": steps, "Calories_Intake": 2000, "Hours_of_Sleep": sleep,
        "Heart_Rate": hr, "Blood_Pressure": bp, "Exercise_Hours_per_Week": exercise,
        "Smoker": smoker, "Alcohol_Consumption_per_Week": alcohol,
        "Diabetic": diabetic, "Heart_Disease": heart_d
    }
    
    try:
        with st.spinner("Our AI is analyzing..."):
            res = requests.post("https://healtharc.onrender.com", json=payload).json()
            
        status = res['status']
        recommendations = res['recommendations']

        # --- DYNAMIC COLOR DIALOG BOX ---
        if status == "Optimal":
            st.success(f"HealthArc Lifestyle Prediction: {status} 🌟")
            st.balloons() # Added a little fun for the best status!
        elif status == "Balanced":
            st.info(f"HealthArc Lifestyle Prediction: {status} ⚖️")
        else: # At Risk
            st.error(f"HealthArc Prediction: {status} ⚠️")

        st.markdown("### 📋 Personalized Guide")
        st.write(recommendations)

    except Exception as e:
        st.error("Could not connect to the Backend. Please ensure uvicorn is running.")