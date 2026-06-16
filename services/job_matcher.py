from datasets.job_roles import JOB_ROLES


def analyze_skill_gap(
    detected_skills,
    selected_role
):
    """
    Compare resume skills
    with selected role
    """

    required_skills = JOB_ROLES[selected_role]

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        if skill in detected_skills:
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    match_score = (
        len(matched_skills)
        / len(required_skills)
    ) * 100

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_score": round(
            match_score,
            2
        )
    }