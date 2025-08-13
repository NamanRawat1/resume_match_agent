# core/scorer.py
def compute_skill_overlap(job_skills: list, resume_skills: list) -> float:
    if not job_skills:
        return 0.0
    set_job = set([s.lower() for s in job_skills])
    set_res = set([s.lower() for s in resume_skills])
    inter = set_job & set_res
    return float(len(inter) / len(set_job))

def combined_score(skill_overlap: float, semantic_sim: float, w_skill: float = 0.6, w_sem: float = 0.4) -> float:
    """
    Inputs are 0..1, output 0..100
    """
    combined = w_skill * skill_overlap + w_sem * semantic_sim
    return round(combined * 100, 1)
