import re


def analyze_ats_resume(
    resume_text,
    matched_skills,
    missing_skills,
    selected_role
):

    text = resume_text.lower()

    score = 0
    strengths = []
    weaknesses = []
    suggestions = []

    # -------------------------------
    # CONTACT INFORMATION
    # -------------------------------

    email_found = re.search(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        text
    )

    phone_found = re.search(
        r"\b\d{10}\b",
        text
    )

    if email_found and phone_found:

        score += 15

        strengths.append(
            "Contact information detected"
        )

    else:

        weaknesses.append(
            "Missing proper contact information"
        )

        suggestions.append(
            "Add email and phone number"
        )

    # -------------------------------
    # LINKEDIN
    # -------------------------------

    if "linkedin" in text:

        score += 8

        strengths.append(
            "LinkedIn profile included"
        )

    else:

        suggestions.append(
            "Add LinkedIn profile"
        )

    # -------------------------------
    # GITHUB (ONLY FOR TECH ROLES)
    # -------------------------------

    technical_roles = [
        "Data Scientist",
        "Machine Learning Engineer",
        "Frontend Developer",
        "Backend Developer",
        "Full Stack Developer"
    ]

    if selected_role in technical_roles:

        if "github" in text:

            score += 8

            strengths.append(
                "GitHub profile included"
            )

        else:

            suggestions.append(
                "Add GitHub profile"
            )

    # -------------------------------
    # EDUCATION SECTION
    # -------------------------------

    education_keywords = [
        "education",
        "b.tech",
        "bachelor",
        "university",
        "college"
    ]

    if any(
        word in text
        for word in education_keywords
    ):

        score += 10

        strengths.append(
            "Education section found"
        )

    else:

        weaknesses.append(
            "Education section missing"
        )

    # -------------------------------
    # PROJECTS SECTION
    # -------------------------------

    if (
        "project" in text
        or "projects" in text
    ):

        score += 10

        strengths.append(
            "Projects section included"
        )

    else:

        weaknesses.append(
            "Projects section missing"
        )

        suggestions.append(
            "Add projects section"
        )

    # -------------------------------
    # SKILL MATCHING
    # -------------------------------

    matched_count = len(
        matched_skills
    )

    score += min(
        matched_count * 4,
        20
    )

    strengths.append(
        f"{matched_count} matching skills found"
    )

    if missing_skills:

        weaknesses.append(
            "Missing critical skills: "
            + ", ".join(
                missing_skills
            )
        )

        suggestions.append(
            "Add missing skills to your resume: "
            + ", ".join(
                missing_skills
            )
        )

    # -------------------------------
    # ACTION VERBS
    # -------------------------------

    action_verbs = [
        "developed",
        "built",
        "created",
        "implemented",
        "optimized",
        "designed",
        "improved",
        "managed"
    ]

    verb_count = sum(
        verb in text
        for verb in action_verbs
    )

    if verb_count >= 2:

        score += 10

        strengths.append(
            "Strong action verbs used"
        )

    else:

        weaknesses.append(
            "Weak action language"
        )

        suggestions.append(
            "Use stronger action verbs"
        )

    # -------------------------------
    # MEASURABLE ACHIEVEMENTS
    # -------------------------------

    achievement_patterns = [
        r"\d+%",
        r"\d+\+",
        r"\d+\s*(users|projects|clients|students)",
        r"(improved|increased|reduced|boosted|optimized)"
    ]

    has_achievement = any(
        re.search(
            pattern,
            text
        )
        for pattern in achievement_patterns
    )

    if has_achievement:

        score += 10

        strengths.append(
            "Quantifiable achievements detected"
        )

    else:

        weaknesses.append(
            "No measurable achievements"
        )

        suggestions.append(
            "Add measurable results"
        )

    # -------------------------------
    # KEYWORD OPTIMIZATION
    # -------------------------------

    if matched_count >= 5:

        score += 10

        strengths.append(
            "Good keyword optimization"
        )

    else:

        weaknesses.append(
            "Weak keyword optimization"
        )

        suggestions.append(
            "Include more job-related keywords"
        )

    # -------------------------------
    # PROFESSIONAL SUMMARY
    # -------------------------------

    summary_keywords = [
        "summary",
        "profile",
        "objective",
        "about me"
    ]

    if any(
        word in text
        for word in summary_keywords
    ):

        score += 9

        strengths.append(
            "Professional summary included"
        )

    else:

        suggestions.append(
            "Add a professional summary"
        )

    # -------------------------------
    # SCORE LIMIT
    # -------------------------------

    score = min(
        score,
        100
    )

    # -------------------------------
    # STATUS
    # -------------------------------

    if score >= 85:

        status = (
            "Excellent ATS Resume"
        )

    elif score >= 70:

        status = (
            "Good Resume"
        )

    elif score >= 50:

        status = (
            "Needs Improvement"
        )

    else:

        status = (
            "Poor ATS Resume"
        )

    return {
        "score": score,
        "status": status,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions
    }