COURSE_DATABASE = {

    # -----------------------------
    # DATA SCIENTIST
    # -----------------------------

    "Data Scientist": {

        "Statistics": {
            "title":
            "Statistics for Data Science",

            "platform":
            "Coursera",

            "link":
            "https://www.coursera.org/learn/statistics-for-data-science-python"
        },

        "NumPy": {
            "title":
            "NumPy for Data Analysis",

            "platform":
            "Udemy",

            "link":
            "https://www.udemy.com/course/python-for-data-science-and-machine-learning-bootcamp/"
        },

        "Machine Learning": {
            "title":
            "Machine Learning by Andrew Ng",

            "platform":
            "Coursera",

            "link":
            "https://www.coursera.org/learn/machine-learning"
        }
    },

    # -----------------------------
    # DATA ANALYST
    # -----------------------------

    "Data Analyst": {

        "SQL": {
            "title":
            "SQL for Data Analysis",

            "platform":
            "Coursera",

            "link":
            "https://www.coursera.org/learn/sql-for-data-science"
        },

        "Excel": {
            "title":
            "Microsoft Excel Data Analysis",

            "platform":
            "Udemy",

            "link":
            "https://www.udemy.com/course/excel-data-analysis/"
        },

        "Power BI": {
            "title":
            "Power BI Full Course",

            "platform":
            "YouTube",

            "link":
            "https://www.youtube.com/watch?v=TmhQCQr_DCA"
        },

        "Statistics": {
            "title":
            "Statistics for Data Analysis",

            "platform":
            "Coursera",

            "link":
            "https://www.coursera.org/learn/basic-statistics"
        }
    },

    # -----------------------------
    # MACHINE LEARNING ENGINEER
    # -----------------------------

    "Machine Learning Engineer": {

        "Machine Learning": {
            "title":
            "Machine Learning Specialization",

            "platform":
            "Coursera",

            "link":
            "https://www.coursera.org/specializations/machine-learning-introduction"
        },

        "Deep Learning": {
            "title":
            "Deep Learning Specialization",

            "platform":
            "Coursera",

            "link":
            "https://www.coursera.org/specializations/deep-learning"
        },

        "TensorFlow": {
            "title":
            "TensorFlow Developer Certificate",

            "platform":
            "Udemy",

            "link":
            "https://www.udemy.com/course/tensorflow-developer-certificate-machine-learning-zero-to-mastery/"
        },

        "Python": {
            "title":
            "Python for Machine Learning",

            "platform":
            "Udemy",

            "link":
            "https://www.udemy.com/course/python-for-data-science-and-machine-learning-bootcamp/"
        }
    },

    # -----------------------------
    # FRONTEND DEVELOPER
    # -----------------------------

    "Frontend Developer": {

        "HTML": {
            "title":
            "HTML Crash Course",

            "platform":
            "YouTube",

            "link":
            "https://www.youtube.com/watch?v=qz0aGYrrlhU"
        },

        "CSS": {
            "title":
            "CSS Complete Guide",

            "platform":
            "Udemy",

            "link":
            "https://www.udemy.com/course/css-the-complete-guide-incl-flexbox-grid-sass/"
        },

        "JavaScript": {
            "title":
            "JavaScript Mastery",

            "platform":
            "Coursera",

            "link":
            "https://www.coursera.org/specializations/javascript-beginner"
        },

        "React": {
            "title":
            "React Complete Course",

            "platform":
            "Udemy",

            "link":
            "https://www.udemy.com/course/react-the-complete-guide-incl-redux/"
        }
    },

    # -----------------------------
    # BACKEND DEVELOPER
    # -----------------------------

    "Backend Developer": {

        "API": {
            "title":
            "REST API Development",

            "platform":
            "Udemy",

            "link":
            "https://www.udemy.com/course/rest-api-flask-and-python/"
        },

        "SQL": {
            "title":
            "SQL Bootcamp",

            "platform":
            "Coursera",

            "link":
            "https://www.coursera.org/learn/sql-for-data-science"
        },

        "Databases": {
            "title":
            "Database Design Fundamentals",

            "platform":
            "Coursera",

            "link":
            "https://www.coursera.org/learn/database-management"
        },

        "Python": {
            "title":
            "Python Backend Development",

            "platform":
            "Udemy",

            "link":
            "https://www.udemy.com/course/python-and-django-full-stack-web-developer-bootcamp/"
        }
    },

    # -----------------------------
    # FULL STACK DEVELOPER
    # -----------------------------

    "Full Stack Developer": {

        "HTML": {
            "title":
            "HTML Full Course",

            "platform":
            "YouTube",

            "link":
            "https://www.youtube.com/watch?v=qz0aGYrrlhU"
        },

        "CSS": {
            "title":
            "CSS Complete Guide",

            "platform":
            "Udemy",

            "link":
            "https://www.udemy.com/course/css-the-complete-guide-incl-flexbox-grid-sass/"
        },

        "JavaScript": {
            "title":
            "JavaScript Bootcamp",

            "platform":
            "Udemy",

            "link":
            "https://www.udemy.com/course/the-complete-javascript-course/"
        },

        "React": {
            "title":
            "React Complete Guide",

            "platform":
            "Udemy",

            "link":
            "https://www.udemy.com/course/react-the-complete-guide-incl-redux/"
        },

        "API": {
            "title":
            "REST API Development",

            "platform":
            "Udemy",

            "link":
            "https://www.udemy.com/course/rest-api-flask-and-python/"
        },

        "SQL": {
            "title":
            "SQL for Developers",

            "platform":
            "Coursera",

            "link":
            "https://www.coursera.org/learn/sql-for-data-science"
        }
    }
}


def recommend_courses(
    selected_role,
    missing_skills
):
    """
    Recommend courses
    based on role
    and missing skills
    """

    recommendations = []

    role_courses = (
        COURSE_DATABASE.get(
            selected_role.strip(),
            {}
        )
    )

    normalized_courses = {

        skill.lower():
        course

        for skill, course
        in role_courses.items()
    }

    for skill in missing_skills:

        normalized_skill = (
            skill.strip().lower()
        )

        if (
            normalized_skill
            in normalized_courses
        ):

            recommendations.append(
                normalized_courses[
                    normalized_skill
                ]
            )

    return recommendations