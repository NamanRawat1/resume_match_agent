# core/agent.py
import json
from anthropic_client import ask_claude
from utils import normalize_text

REPORT_PROMPT_TEMPLATE = """
You are an expert hiring assistant. Given the following, produce a JSON object EXACTLY with keys:
  - match_score: float (0-100)
  - summary: short text explaining fit
  - strengths: array of strings
  - gaps: array of strings
  - improvements: array of actionable resume edits

Input data:

Job Description:
{job_text}

Extracted Job Skills:
{job_skills}

Resume (snippet):
{resume_snippet}

Extracted Resume Skills:
{resume_skills}

Computed signals:
skill_overlap={skill_overlap:.3f}
semantic_similarity={semantic_similarity:.3f}
estimated_match_score={estimated_score}

Return JSON ONLY.
"""

def generate_report(job_text: str, job_skills: list, resume_text: str, resume_skills: list,
                    skill_overlap: float, semantic_similarity: float, estimated_score: float):
    # prepare inputs (normalize & shorten the resume snippet)
    resume_snippet = normalize_text(resume_text)[:2000]
    prompt = REPORT_PROMPT_TEMPLATE.format(
        job_text=job_text,
        job_skills=json.dumps(job_skills, indent=2),
        resume_snippet=resume_snippet,
        resume_skills=json.dumps(resume_skills, indent=2),
        skill_overlap=skill_overlap,
        semantic_similarity=semantic_similarity,
        estimated_score=estimated_score
    )

    resp = ask_claude(prompt, max_tokens=600)
    # try to parse JSON
    try:
        start = resp.find("{")
        end = resp.rfind("}")
        if start != -1 and end != -1 and end > start:
            js = resp[start:end+1]
            data = json.loads(js)
            return data
    except Exception:
        pass

    # fallback minimal report
    return {
        "match_score": estimated_score,
        "summary": f"Skill overlap {skill_overlap:.2f}, semantic sim {semantic_similarity:.2f}",
        "strengths": resume_skills[:5],
        "gaps": [s for s in job_skills if s.lower() not in [r.lower() for r in resume_skills]],
        "improvements": ["Add relevant bullet points emphasizing the missing skills."]
    }
