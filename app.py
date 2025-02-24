import streamlit as st
import requests
import numpy as np

# FastAPI Backend URL (Replace with your deployed API URL)
API_URL = "https://web-production-4999.up.railway.app/predict"

# Streamlit UI Configuration
st.set_page_config(page_title="Diabetes Prediction", layout="centered")

st.title("🩺 Diabetes Prediction App")
st.markdown("### Enter the required health parameters to predict diabetes.")

# Define input fields with labels
columns = ["Pregnancies", "Glucose", "Blood Pressure", "Skin Thickness", "Insulin", "BMI", "Diabetes Pedigree", "Age"]
values = []

# Create input fields
with st.form("diabetes_form"):
    col1, col2 = st.columns(2)
    for i, col in enumerate(columns):
        value = col1.number_input(col, min_value=0.0, step=0.1, key=col) if i % 2 == 0 else col2.number_input(col, min_value=0.0, step=0.1, key=col)
        values.append(value)
    
    # Buttons
    submit_btn = st.form_submit_button("Predict")
    clear_btn = st.form_submit_button("Clear")

# Handle clear button
if clear_btn:
    st.rerun()  # ✅ Fix: Use `st.rerun()` instead of `st.experimental_rerun()`

# Handle predict button
if submit_btn:
    try:
        processing_msg = st.info("🔄 Processing... Please wait!")  # Show loading message

        response = requests.post(API_URL, json={"feature_values": values})
        result = response.json()

        processing_msg.empty()
        # Display Prediction Result
        if "prediction" in result:
            st.success(f"✅ {result['prediction']}")
        else:
            st.error("⚠️ Error in prediction. Please check inputs.")
    except Exception as e:
        st.error(f"❌ API Error: {str(e)}")
