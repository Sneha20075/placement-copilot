"""
Custom function-tools for the Placement Copilot agents.
ADK auto-wraps plain Python functions into FunctionTools as long as they
have type hints and a clear docstring (the LLM reads the docstring to
decide when/how to call the tool).
"""

from datetime import date, datetime
import re

# A tiny in-memory "skills database" per target role.
# In a real deployment this would come from a DB / scraped job postings.
ROLE_SKILL_MAP = {
    "ai/ml engineer": ["Python", "SQL", "Pandas", "NumPy", "Scikit-learn",
                        "PyTorch/TensorFlow", "ML system design", "Statistics"],
    "genai engineer": ["Python", "LLM fundamentals", "Prompt engineering",
                        "RAG", "LangChain/LlamaIndex", "Vector DBs",
                        "Agent frameworks (ADK/LangGraph)", "APIs"],
    "sde": ["DSA", "OOPS", "DBMS", "OS", "Computer Networks", "System Design",
            "Git", "One backend framework"],
}


def check_skill_gap(target_role: str, current_skills: str) -> dict:
    """Compares the student's current skills against what a target role
    typically requires, and returns the missing skills.

    Args:
        target_role: The role the student is targeting, e.g. "AI/ML Engineer",
            "GenAI Engineer", or "SDE".
        current_skills: Comma-separated list of skills the student already has.

    Returns:
        A dict with 'have', 'missing', and 'match_percent' keys.
    """
    role_key = target_role.strip().lower()
    required = ROLE_SKILL_MAP.get(role_key, ROLE_SKILL_MAP["ai/ml engineer"])
    have = {s.strip().lower() for s in current_skills.split(",") if s.strip()}
    missing = [s for s in required if s.lower() not in have]
    matched = len(required) - len(missing)
    match_percent = round((matched / len(required)) * 100, 1) if required else 0.0
    return {
        "target_role": target_role,
        "have": sorted(have),
        "missing": missing,
        "match_percent": match_percent,
    }


def days_until(target_date: str) -> dict:
    """Calculates how many days are left until a target date (e.g. a
    placement drive or exam date).

    Args:
        target_date: Date string in YYYY-MM-DD format.

    Returns:
        A dict with 'days_remaining' and 'weeks_remaining'.
    """
    today = date.today()
    try:
        target = datetime.strptime(target_date, "%Y-%m-%d").date()
    except ValueError:
        return {"error": "target_date must be in YYYY-MM-DD format"}
    delta = (target - today).days
    return {
        "days_remaining": max(delta, 0),
        "weeks_remaining": round(max(delta, 0) / 7, 1),
    }


def estimate_resume_ats_score(resume_text: str, job_description: str) -> dict:
    """Gives a rough ATS (Applicant Tracking System) keyword-match score by
    comparing resume text against a job description's keywords. This is a
    lightweight heuristic, not a replacement for a real ATS.

    Args:
        resume_text: Plain text of the student's resume.
        job_description: Plain text of the target job description.

    Returns:
        A dict with 'score_percent' and 'missing_keywords'.
    """
    def tokenize(text: str) -> set:
        words = re.findall(r"[a-zA-Z][a-zA-Z0-9+.#]{2,}", text.lower())
        stopwords = {"the", "and", "for", "with", "you", "are", "our", "will",
                     "this", "that", "have", "your", "who", "job", "role"}
        return {w for w in words if w not in stopwords}

    jd_words = tokenize(job_description)
    resume_words = tokenize(resume_text)
    if not jd_words:
        return {"score_percent": 0.0, "missing_keywords": []}

    matched = jd_words & resume_words
    missing = sorted(jd_words - resume_words)[:15]  # cap for readability
    score = round((len(matched) / len(jd_words)) * 100, 1)
    return {"score_percent": score, "missing_keywords": missing}
