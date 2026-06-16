LEARNING_RESOURCES = {

    "Statistics": {
        "topics": [
            "Mean",
            "Median",
            "Probability",
            "Distributions"
        ],
        "resource":
        "Statistics for Data Science"
    },

    "NumPy": {
        "topics": [
            "Arrays",
            "Indexing",
            "Broadcasting",
            "Vectorization"
        ],
        "resource":
        "NumPy Basics"
    },

    "Pandas": {
        "topics": [
            "DataFrames",
            "Filtering",
            "Grouping",
            "Merging"
        ],
        "resource":
        "Pandas Full Course"
    },

    "HTML": {
        "topics": [
            "Tags",
            "Forms",
            "Semantic HTML"
        ],
        "resource":
        "HTML Crash Course"
    },

    "CSS": {
        "topics": [
            "Flexbox",
            "Grid",
            "Responsive Design"
        ],
        "resource":
        "CSS Full Course"
    },

    "JavaScript": {
        "topics": [
            "Variables",
            "DOM",
            "Functions",
            "Async JS"
        ],
        "resource":
        "JavaScript Essentials"
    },

    "React": {
        "topics": [
            "Components",
            "Hooks",
            "Props",
            "State Management"
        ],
        "resource":
        "React for Beginners"
    },

    "SQL": {
        "topics": [
            "SELECT",
            "JOIN",
            "GROUP BY",
            "Subqueries"
        ],
        "resource":
        "SQL Complete Course"
    },

    "Python": {
        "topics": [
            "Functions",
            "Loops",
            "OOP",
            "Libraries"
        ],
        "resource":
        "Python for Everybody"
    }
}


def get_learning_recommendations(
    missing_skills
):
    recommendations = {}

    for skill in missing_skills:

        if skill in LEARNING_RESOURCES:

            recommendations[
                skill
            ] = (
                LEARNING_RESOURCES[
                    skill
                ]
            )

    return recommendations