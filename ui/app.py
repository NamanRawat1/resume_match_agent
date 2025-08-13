# ui/app.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
import tempfile, os, json
from match_logic import match_resume_to_job
from db import init_db, save_result
from utils import extract_text_from_pdf


init_db()
st.title("Resume → Job Match Agent")

uploaded_resume = st.file_uploader("Upload resume PDF", type=["pdf"])
uploaded_job = st.file_uploader("Upload job description (.txt)", type=["txt"])

if uploaded_resume and uploaded_job:
    if st.button("Run match"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_resume.read())
            resume_path = tmp.name
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp2:
            tmp2.write(uploaded_job.read())
            job_path = tmp2.name

        resume_text = extract_text_from_pdf(resume_path)
        with open(job_path, "r", encoding="utf-8") as f:
            job_text = f.read()

        report = match_resume_to_job(resume_text, job_text)
        st.subheader("Match Report")
        st.json(report)

        save_result(resume_path, job_path, report)
        st.success("Saved to DB (if configured).")

        # cleanup
        os.unlink(resume_path)
        os.unlink(job_path)
