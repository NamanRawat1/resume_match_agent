# match_logic.py
from core.extractor import extract_structured_info
from core.similarity import compute_tfidf_similarity
from core.scorer import compute_skill_overlap, combined_score
from core.agent import generate_report
from utils import normalize_text  # newly added import

def match_resume_to_job(resume_text: str, job_text: str):
    # Extract structured info
    job_struct = extract_structured_info(job_text, kind="job")
    resume_struct = extract_structured_info(resume_text, kind="resume")

    job_skills = job_struct.get("required_skills") or job_struct.get("skills") or []
    resume_skills = resume_struct.get("skills") or []

    # Similarity (0..1)
    semantic_sim = compute_tfidf_similarity(resume_text, job_text)

    # Skill overlap (0..1)
    skill_overlap = compute_skill_overlap(job_skills, resume_skills)

    # Final combined score 0..100
    final = combined_score(skill_overlap, semantic_sim)

    # Ask agent to produce JSON report
    report = generate_report(
        job_text=job_text,
        job_skills=job_skills,
        resume_text=resume_text,
        resume_skills=resume_skills,
        skill_overlap=skill_overlap,
        semantic_similarity=semantic_sim,
        estimated_score=final
    )
    return report

def match_resume_against_jobs(resume_text: str, jobs: list, top_n=5):
    results = []
    for job in jobs:
        job_text = normalize_text(job["description"])
        report = match_resume_to_job(resume_text, job_text)
        report.update({"title": job["title"], "url": job.get("url", "")})
        results.append(report)
    results.sort(key=lambda r: r["match_score"], reverse=True)
    return results[:top_n]
