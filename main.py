# main.py
import os
from dotenv import load_dotenv
from utils import extract_text_from_pdf
from match_logic import match_resume_to_job
from db import init_db, save_result
import json

load_dotenv()

def main():
    init_db()  # ensure tables exist

    resume_path = input("Enter path to resume PDF: ").strip()
    if not os.path.exists(resume_path):
        print("Resume file not found:", resume_path)
        return

    job_path = input("Enter path to job description .txt: ").strip()
    if not os.path.exists(job_path):
        print("Job description file not found:", job_path)
        return

    resume_text = extract_text_from_pdf(resume_path)
    with open(job_path, "r", encoding="utf-8") as f:
        job_text = f.read()

    print("Running matching pipeline (this may call Claude and take a few seconds)...")
    report = match_resume_to_job(resume_text, job_text)
    print("\n=== Match Report ===")
    print(json.dumps(report, indent=2))

    # persist to DB
    save_result(resume_path, job_path, report)
    print("Saved match result to DB.")

if __name__ == "__main__":
    main()
