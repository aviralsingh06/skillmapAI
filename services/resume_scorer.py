def calculate_resume_score(
    match_score,
    skills,
    missing_skills,
    extracted_text
):
    """
    Calculate resume strength score
    """

    score = 0

    # Job match contribution
    score += match_score * 0.5

    # Skill count
    score += min(len(skills) * 2, 20)

    # Penalize missing skills
    score -= len(missing_skills) * 2

    # Project detection
    if "project" in extracted_text.lower():
        score += 10

    # GitHub / Kaggle bonus
    if (
        "github" in extracted_text.lower()
        or
        "kaggle" in extracted_text.lower()
    ):
        score += 10

    return max(
        0,
        min(round(score), 100)
    )