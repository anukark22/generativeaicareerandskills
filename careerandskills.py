import streamlit as st
import requests
import json
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Generative AI for Career & Skills",
    page_icon="🎓",
    layout="wide",
)

# --- Title and Description ---
# This is the line that sets the title. It has been corrected.
st.title("Career Advisor 🎓")
st.markdown("Enter your current skills and a desired career path to receive a personalized roadmap to success.")

# --- User Inputs ---
with st.container():
    st.subheader("Your Information")
    current_skills = st.text_area(
        "List your current skills (e.g., Python, teamwork, data analysis, communication)",
        height=100
    )
    desired_career = st.text_input(
        "What is your desired career? (e.g., Data Scientist, Marketing Manager, UX Designer)"
    )

# --- AI Interaction ---
if st.button("Generate My Career Plan"):
    if not current_skills or not desired_career:
        st.error("Please fill in both fields to get your personalized plan.")
    else:
        with st.spinner("Analyzing your skills and generating a career plan..."):
            try:
                # The detailed prompt for the Gemma model
                prompt = f"""
                You are an expert career counselor and mentor. Your goal is to guide students towards their highest potential.

                A student has provided their current skills and a desired career path. Your task is to provide a comprehensive and actionable plan.

                Student's Current Skills:
                {current_skills}

                Desired Career Path:
                {desired_career}

                Your output must be structured with clear headings and a professional, encouraging tone. Include the following sections, with details for each:

                ### Skill Gap Analysis
                Identify the key hard skills, soft skills, and specific knowledge areas that the student is missing to succeed in the desired career. Be specific and provide concrete examples.

                ### Personalized Learning Roadmap
                Create a step-by-step roadmap to bridge the identified skill gaps. For each skill, suggest specific actions such as online courses, certifications, personal projects, books, or practice exercises.

                ### Job Market Preparation
                Provide actionable advice on how to prepare for the job market, including tips on resume building, networking, and interview preparation. Suggest specific questions the student should be ready to answer in an interview for the target role.
                """
                
                # This is the key part: it connects to your local Ollama server, NOT OpenAI.
                api_url = "http://localhost:11434/api/generate"
                payload = {
                    "model": "gemma:2b",  # This specifies the model you are using
                    "prompt": prompt,
                    "stream": False,
                }
                
                response = requests.post(api_url, json=payload)
                response_data = response.json()
                
                ai_output = response_data.get("response", "")

                st.subheader("Your Personalized Career Plan 🚀")
                st.markdown(ai_output)
                
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to Ollama. Make sure Ollama is running in your terminal and that you've run the 'ollama run gemma:2b' command.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")