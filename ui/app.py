# ui/app.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from utils import extract_text_from_pdf
from scraper import fetch_naukri_jobs
from match_logic import match_resume_against_jobs
import urllib.parse

st.set_page_config(page_title="Resume Matcher", layout="wide")

st.title("📄 Resume vs Naukri Job Matcher")
st.markdown("Upload your resume and find the **best matching jobs** from Naukri.com.")

# --- Search keyword input ---
default_keyword = "senior software engineer"
keyword = st.text_input("Job Search Keyword", value=default_keyword)
num_pages = st.slider("Pages to fetch from Naukri", min_value=1, max_value=5, value=2)

# File uploader
uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

if uploaded_file is not None:
    # Encode keyword into Naukri search URL
    search_query = urllib.parse.quote(keyword)
    naukri_url = f"https://www.naukri.com/{search_query}-jobs?k={search_query}"

    with st.spinner("Extracting text from your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    with st.spinner(f"Fetching jobs for '{keyword}' from Naukri..."):
        jobs = fetch_naukri_jobs(naukri_url, num_pages=num_pages)

    if not jobs:
        st.error("No jobs found. Try another keyword.")
    else:
        st.success(f"Fetched {len(jobs)} jobs from Naukri.")

        with st.spinner("Matching jobs..."):
            matches = match_resume_against_jobs(resume_text, jobs, top_n=10)

        st.subheader("🏆 Top 10 Job Matches")
        for idx, m in enumerate(matches, 1):
            st.markdown(f"### {idx}. [{m['title']}]({m['url']})")
            st.write(f"**Score:** {m['match_score']}")
            st.write(f"**Summary:** {m['summary']}")
            st.write("---")
