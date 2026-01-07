import os
from dotenv import load_dotenv

load_dotenv()   # <-- MUST be before anything else

import streamlit as st
from openai import OpenAI

from pypdf import PdfReader

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

st.title("AI Resume Analyzer & Job Match Assistant")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

resume_text = ""

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        resume_text += page.extract_text()
else:
    resume_text = st.text_area("Or paste resume text here")

job_description = st.text_area("Paste Job Description Here")

if st.button("Analyze Resume"):
    if resume_text and job_description:
        with st.spinner("Analyzing resume with AI..."):
            prompt = f"""
You are an AI hiring assistant.

Analyze the resume against the job description and provide:

1. Resume Match Score (0–100%)
2. Short match summary
3. Missing or weak skills
4. 3 resume improvement suggestions

Rules:
- Score must be a number between 0 and 100
- Clearly mention "Match Score:" in output

Resume:
{resume_text}

Job Description:
{job_description}
"""

            response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.2
)


            st.success("Analysis Complete")
            st.write(response.choices[0].message.content)
    else:
        st.warning("Please paste both resume and job description.")
