def create_roadmap(
    missing_skills
):
    """
    Generate learning roadmap
    based on missing skills
    """

    roadmap = []

    for index, skill in enumerate(
        missing_skills,
        start=1
    ):

        # Priority logic
        if index == 1:
            priority = "High"
            duration = "7 Days"

        elif index == 2:
            priority = "Medium"
            duration = "5 Days"

        else:
            priority = "Low"
            duration = "3 Days"

        roadmap.append(
            {
                "step": index,
                "skill": skill,
                "priority": priority,
                "duration": duration
            }
        )

    return roadmap