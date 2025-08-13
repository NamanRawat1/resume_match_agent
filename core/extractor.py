# core/extractor.py
import json
import re
from anthropic_client import ask_claude
from utils import normalize_text

AI_PROMPT_TEMPLATE = """
You are a resume/job parsing assistant. Given the text, return JSON ONLY with keys relevant below.

If kind == "resume":
  return {{ "skills": [...], "summary": "short summary (1-2 sentences)" }}

If kind == "job":
  return {{ "required_skills": [...], "responsibilities": [...] }}

Text:
\"\"\"{text}\"\"\"
"""

def extract_structured_info(text: str, kind: str = "resume") -> dict:
    """
    Attempts to extract structured info using Claude. Falls back to heuristics.
    """
    text = normalize_text(text)[:4000]  # limit
    prompt = AI_PROMPT_TEMPLATE.format(text=text)
    try:
        resp = ask_claude(prompt, max_tokens=400)
        # extract JSON object from response
        start = resp.find("{")
        end = resp.rfind("}")
        if start != -1 and end != -1 and end > start:
            js = resp[start:end+1]
            data = json.loads(js)
            # normalize keys depending on kind
            if kind == "resume":
                data.setdefault("skills", [])
                data.setdefault("summary", "")
            else:
                data.setdefault("required_skills", [])
                data.setdefault("responsibilities", [])
            return data
    except Exception:
        pass

    # Fallback heuristics
    if kind == "resume":
        return {"skills": fallback_skill_extract(text), "summary": ""}
    else:
        return {"required_skills": fallback_skill_extract(text), "responsibilities": []}

def fallback_skill_extract(text: str):
    text_low = text.lower()
    seed = ["python","java","sql","aws","docker","kubernetes","nlp","pytorch","tensorflow","react","node","javascript","aws","gcp"]
    found = []
    for s in seed:
        if re.search(rf"\b{s}\b", text_low):
            found.append(s)
    # dedupe & return
    return list(dict.fromkeys(found))
