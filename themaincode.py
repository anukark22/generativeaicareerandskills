import streamlit as st
import requests
import json
import os


st.set_page_config(
    page_title="Generative AI for Career & Skills",
    page_icon="",
    layout="wide",
)


st.title("Hope: Career Advisor ")
st.markdown("Enter your current skills and a desired career path to receive a personalized roadmap to success.")


with st.container():
    st.subheader("Your Information")
    current_skills = st.text_area(
        "List your current skills (e.g., Python, teamwork, data analysis, communication)",
        height=100
    )
    desired_career = st.text_input(
        "What is your desired career? (e.g., Data Scientist, Marketing Manager, UX Designer)"
    )


if st.button("Generate My Career Plan"):
    if not current_skills or not desired_career:
        st.error("Please fill in both fields to get your personalized plan.")
    else:
        with st.spinner("Analyzing your skills and generating a career plan..."):
            try:
                
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
                Create a step-by-step roadmap to bridge the identified skill gaps. For each skill, suggest specific actions such as **online courses, named certifications (e.g., Google Data Analytics Professional Certificate), personal projects, books, or practice exercises**.

                ### Job Market Preparation
                Provide actionable advice on how to prepare for the job market, including tips on resume building, networking, and interview preparation. Suggest specific questions the student should be ready to answer in an interview for the target role.
                """
                
                api_url = "http://localhost:11434/api/generate"
                payload = {
                    "model": "gemma:2b",
                    "prompt": prompt,
                    "stream": False,
                }
                
                response = requests.post(api_url, json=payload)
                response_data = response.json()
                
                ai_output = response_data.get("response", "")

                st.subheader("Your Personalized Career Plan ")
                st.markdown(ai_output)
                
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to Ollama. Make sure Ollama is running in your terminal and that you've run the 'ollama run gemma:2b' command.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")


st.markdown("---")
st.subheader("Connect to Opportunities ")
st.markdown("Find the right places to look for jobs and build your network.")

if st.button("Find Opportunities"):
    if not desired_career:
        st.error("Please enter a desired career path above.")
    else:
        with st.spinner("Searching for relevant opportunities..."):
            try:
                prompt_opportunities = f"""
                You are an expert career placement specialist. Given the desired career path of '{desired_career}', provide a comprehensive guide to finding opportunities.

                Your output must include:
                - A list of the top **3-5 job boards** or platforms that are highly relevant for this career.
                - A list of **2-3 professional organizations or communities** (e.g., for networking, knowledge sharing, mentorship).
                - A list of **3-5 types of companies or industries** that typically hire for this role.
                """
                
                api_url = "http://localhost:11434/api/generate"
                payload = {
                    "model": "gemma:2b",
                    "prompt": prompt_opportunities,
                    "stream": False,
                }
                
                response = requests.post(api_url, json=payload)
                response_data = response.json()
                ai_output = response_data.get("response", "")

                st.subheader("Your Opportunity Roadmap ")
                st.markdown(ai_output)
            except Exception as e:
                st.error(f"An error occurred while generating the opportunity roadmap: {e}")


st.markdown("---")
st.subheader("Interview Question Practice ")
st.markdown("Prepare for your interviews by generating common questions and advice.")
interview_button = st.button("Generate Interview Questions")

if interview_button:
    if not desired_career:
        st.error("Please enter your desired career path above.")
    else:
        with st.spinner("Generating interview questions..."):
            try:
                prompt_interview = f"""
                You are an experienced hiring manager for the role of {desired_career}. Your task is to provide a student with a list of common interview questions.

                Generate a list of at least 5 common technical and behavioral interview questions for the {desired_career} role.
                For each question, provide a brief, high-level tip on how to structure a good answer.
                """
                
                api_url = "http://localhost:11434/api/generate"
                payload = {
                    "model": "gemma:2b",
                    "prompt": prompt_interview,
                    "stream": False,
                }
                
                response = requests.post(api_url, json=payload)
                response_data = response.json()
                ai_output = response_data.get("response", "")

                st.subheader("Common Interview Questions for Your Role ")
                st.markdown(ai_output)
            except Exception as e:
                st.error(f"An error occurred while generating questions: {e}")