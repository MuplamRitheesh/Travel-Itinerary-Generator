import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv


# ==========================================
# Load API Key
# ==========================================
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ GOOGLE_API_KEY not found in .env file")
    st.stop()

genai.configure(api_key=API_KEY)


# ==========================================
# Find Available Model Automatically
# ==========================================
def get_model():
    try:
        models = genai.list_models()

        for m in models:
            if "generateContent" in m.supported_generation_methods:
                return genai.GenerativeModel(m.name)

    except Exception as e:
        st.error(f"Model discovery failed:\n{e}")

    return None


model = get_model()

if model is None:
    st.error("❌ No compatible Gemini model available.")
    st.stop()


# ==========================================
# AI Generator
# ==========================================
def generate_itinerary(destination, days, nights):

    prompt = f"""
    Write a detailed travel blog itinerary.

    Destination: {destination}
    Duration: {days} days and {nights} nights

    Include:
    - Day-wise schedule
    - Tourist attractions
    - Local food suggestions
    - Budget tips
    - Safety tips
    - Friendly storytelling tone
    """

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"⚠️ Gemini API Error:\n{e}"


# ==========================================
# Streamlit UI
# ==========================================
def main():

    st.set_page_config(page_title="AI Travel Planner")

    st.title("🌍 AI Travel Itinerary Generator")
  # Inputs
    destination = st.text_input("Enter your desired destination:")
    days = st.number_input("Enter the number of days:", min_value=1)
    nights = st.number_input("Enter the number of nights:", min_value=0)

    if st.button("Generate Itinerary"):

        if destination.strip():
            with st.spinner("Generating..."):
                result = generate_itinerary(destination, days, nights)

            st.text_area("Result", result, height=400)

        else:
            st.warning("Enter destination")


# ==========================================
# Run
# ==========================================
if __name__ == "__main__":
    main()
