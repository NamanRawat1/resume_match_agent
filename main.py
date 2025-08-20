# main.py (modified)
from scraper import fetch_naukri_jobs
from utils import extract_text_from_pdf
from match_logic import match_resume_against_jobs
import json
import os

if __name__ == "__main__":
    resume_path = input("Enter path to resume PDF: ").strip()
    if not os.path.exists(resume_path):
        print(f"❌ Resume file not found: {resume_path}")
        exit(1)

    url = input("Enter Naukri search URL: ").strip()
    if not url.startswith("http"):
        print("❌ Please enter a valid Naukri job search URL.")
        exit(1)

    try:
        resume_text = extract_text_from_pdf(resume_path)
    except Exception as e:
        print(f"❌ Error reading resume: {e}")
        exit(1)

    print("📡 Fetching job listings...")
    jobs = fetch_naukri_jobs(url, num_pages=2)
    if not jobs:
        print("⚠ No jobs found from the given URL.")
        exit(0)

    print(f"✅ Fetched {len(jobs)} jobs. Matching against resume...")
    matches = match_resume_against_jobs(resume_text, jobs, top_n=10)

    print("\n=== Top Matches ===")
    for idx, m in enumerate(matches, 1):
        print(f"{idx}. {m['title']} – Score: {m['match_score']}")
        print(f"   Summary: {m.get('summary', '')}")
        print(f"   URL: {m.get('url', '')}\n")
