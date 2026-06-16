def generate_resume_suggestions(
    extracted_text,
    selected_role,
    missing_skills
):
    """
    Generate resume suggestions
    """

    suggestions = []

    if missing_skills:
        suggestions.append(
            "Add missing skills to your resume: "
            + ", ".join(missing_skills)
        )

    if (
        "machine learning"
        in selected_role.lower()
        or
        "data scientist"
        in selected_role.lower()
    ):
        suggestions.append(
            "Add machine learning projects"
        )

        suggestions.append(
            "Include statistics and data analysis experience"
        )

        suggestions.append(
            "Mention Kaggle or GitHub projects"
        )

    if (
        "frontend"
        in selected_role.lower()
    ):
        suggestions.append(
            "Build UI projects using React and JavaScript"
        )

        suggestions.append(
            "Add portfolio website link"
        )

    suggestions.append(
        "Add measurable achievements in projects"
    )

    suggestions.append(
        "Improve resume summary based on target role"
    )

    return suggestions