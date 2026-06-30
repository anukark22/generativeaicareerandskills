import streamlit as st
import requests

st.set_page_config(
    page_title="Generative AI for Career & Skills",
    page_icon="🎯",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Sidebar: Ollama connection settings (lets the user point at the right
# host/model instead of hard-coding values that may not match their setup)
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Ollama Settings")
    ollama_host = st.text_input("Ollama host URL", value="http://localhost:11434")
    model_name = st.text_input("Model name", value="gemma:2b")
    st.caption("Make sure Ollama is running and the model has been pulled, "
               "e.g. `ollama pull gemma:2b`.")

# ---------------------------------------------------------------------------
# Helper: single place that talks to Ollama, with proper error handling
# ---------------------------------------------------------------------------
def call_ollama(prompt: str, model: str, host: str, timeout: int = 120) -> str:
    """
    Calls the local Ollama /api/generate endpoint and returns the generated
    text. Raises a RuntimeError with a friendly message on any failure so
    the caller can just show it with st.error().
    """
    api_url = f"{host.rstrip('/')}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    try:
        response = requests.post(api_url, json=payload, timeout=timeout)
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Could not connect to Ollama. Make sure Ollama is running "
            f"(`ollama serve`) and reachable at {host}."
        )
    except requests.exceptions.Timeout:
        raise RuntimeError(
            "The request to Ollama timed out. The model may still be "
            "loading, or your machine may need more time — try again."
        )

    # Ollama returns non-200 status codes (e.g. model not found) with a
    # JSON body containing an "error" field.
    if response.status_code != 200:
        try:
            err_msg = response.json().get("error", response.text)
        except ValueError:
            err_msg = response.text
        raise RuntimeError(f"Ollama returned an error: {err_msg}")

    try:
        response_data = response.json()
    except ValueError:
        raise RuntimeError("Ollama returned a response that wasn't valid JSON.")

    if "error" in response_data:
        raise RuntimeError(f"Ollama returned an error: {response_data['error']}")

    ai_output = response_data.get("response", "").strip()
    if not ai_output:
        raise RuntimeError("Ollama returned an empty response. Try again.")

    return ai_output


# ---------------------------------------------------------------------------
# Session state so results from earlier button clicks don't disappear when
# a different button is clicked later (Streamlit reruns the whole script
# on every interaction, so without this each result would vanish).
# ---------------------------------------------------------------------------
for key in ("career_plan", "opportunities", "interview_questions"):
    if key not in st.session_state:
        st.session_state[key] = None

st.title("Hope: Career Advisor 🎯")
st.markdown(
    "Enter your current skills and a desired career path to receive a "
    "personalized roadmap to success."
)

with st.container():
    st.subheader("Your Information")
    current_skills = st.text_area(
        "List your current skills (e.g., Python, teamwork, data analysis, communication)",
        height=100,
    )
    desired_career = st.text_input(
        "What is your desired career? (e.g., Data Scientist, Marketing Manager, UX Designer)"
    )

# ---------------------------------------------------------------------------
# 1. Career plan
# ---------------------------------------------------------------------------
if st.button("Generate My Career Plan"):
    if not current_skills or not desired_career:
        st.error("Please fill in both fields to get your personalized plan.")
    else:
        with st.spinner("Analyzing your skills and generating a career plan..."):
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
            try:
                st.session_state["career_plan"] = call_ollama(prompt, model_name, ollama_host)
            except RuntimeError as e:
                st.session_state["career_plan"] = None
                st.error(str(e))

if st.session_state["career_plan"]:
    st.subheader("Your Personalized Career Plan 📋")
    st.markdown(st.session_state["career_plan"])

st.markdown("---")

# ---------------------------------------------------------------------------
# 2. Opportunities
# ---------------------------------------------------------------------------
st.subheader("Connect to Opportunities 🌐")
st.markdown("Find the right places to look for jobs and build your network.")

if st.button("Find Opportunities"):
    if not desired_career:
        st.error("Please enter a desired career path above.")
    else:
        with st.spinner("Searching for relevant opportunities..."):
            prompt_opportunities = f"""
You are an expert career placement specialist. Given the desired career path of '{desired_career}', provide a comprehensive guide to finding opportunities.

Your output must include:
- A list of the top **3-5 job boards** or platforms that are highly relevant for this career.
- A list of **2-3 professional organizations or communities** (e.g., for networking, knowledge sharing, mentorship).
- A list of **3-5 types of companies or industries** that typically hire for this role.
"""
            try:
                st.session_state["opportunities"] = call_ollama(
                    prompt_opportunities, model_name, ollama_host
                )
            except RuntimeError as e:
                st.session_state["opportunities"] = None
                st.error(str(e))

if st.session_state["opportunities"]:
    st.subheader("Your Opportunity Roadmap 🗺️")
    st.markdown(st.session_state["opportunities"])

st.markdown("---")

# ---------------------------------------------------------------------------
# 3. Interview questions
# ---------------------------------------------------------------------------
st.subheader("Interview Question Practice 🗣️")
st.markdown("Prepare for your interviews by generating common questions and advice.")

if st.button("Generate Interview Questions"):
    if not desired_career:
        st.error("Please enter your desired career path above.")
    else:
        with st.spinner("Generating interview questions..."):
            prompt_interview = f"""
You are an experienced hiring manager for the role of {desired_career}. Your task is to provide a student with a list of common interview questions.

Generate a list of at least 5 common technical and behavioral interview questions for the {desired_career} role.
For each question, provide a brief, high-level tip on how to structure a good answer.
"""
            try:
                st.session_state["interview_questions"] = call_ollama(
                    prompt_interview, model_name, ollama_host
                )
            except RuntimeError as e:
                st.session_state["interview_questions"] = None
                st.error(str(e))

if st.session_state["interview_questions"]:
    st.subheader("Common Interview Questions for Your Role ❓")
    st.markdown(st.session_state["interview_questions"])