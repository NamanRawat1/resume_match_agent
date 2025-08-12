import os
from dotenv import load_dotenv
from anthropic import Anthropic
from utils import extract_text_from_pdf
import httpx

load_dotenv()

http_client = httpx.Client(verify=False)
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"),http_client=http_client)

def match_resume_to_job(resume_text, job_text):
    prompt = f"""
    You are an AI Job Match Assistant.
    Given a resume and a job description, analyze the match score (0–100),
    explain why, and suggest improvements for the resume.

    Resume:
    {resume_text}

    Job Description:
    {job_text}

    Respond in JSON with:
    {{
      "match_score": <score>,
      "summary": "<summary>",
      "suggestions": ["<point1>", "<point2>", ...]
    }}
    """
    resp = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return resp.content[0].text


if __name__ == "__main__":
    resume_path = input("Enter path to resume PDF: ").strip()
    job_desc_path = input("Enter path to job description .txt file: ").strip()

    if not os.path.exists(resume_path):
        print("❌ Resume file not found.")
        exit()

    if not os.path.exists(job_desc_path):
        print("❌ Job description file not found.")
        exit()

    resume_text = extract_text_from_pdf(resume_path)

    with open(job_desc_path, "r", encoding="utf-8") as f:
        job_text = f.read()

    result = match_resume_to_job(resume_text, job_text)

    print("\n=== AI Match Result ===")
    print(result)
