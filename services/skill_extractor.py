from datasets.skills_list import SKILLS_DATABASE


def extract_skills(resume_text):
    """
    Extract skills from resume text
    """

    detected_skills = []

    resume_text = resume_text.lower()

    for skill in SKILLS_DATABASE:

        if skill.lower() in resume_text:
            detected_skills.append(skill)

    return list(set(detected_skills))