# SkillMap AI

SkillMap AI is an AI-powered Resume Intelligence Platform that helps students, freshers, and job seekers analyze resumes, improve ATS scores, identify skill gaps, and generate personalized learning roadmaps.

The platform combines Resume Analysis, ATS Evaluation, Skill Gap Intelligence, Learning Recommendations, and Career Development Insights into a single dashboard.

---

# 🔑 Getting Started

### New Users

1. Open the application.
2. Click **Sign Up**.
3. Enter:
   - Full Name
   - Email Address
   - Password (minimum 6 characters)
4. Click **Create Account**.
5. Login using your newly created credentials.

### Existing Users

1. Click **Login**.
2. Enter your registered email and password.
3. Click **Sign In**.

### Forgot Password

1. Open the **Forgot Password** tab.
2. Enter your registered email.
3. Click **Send Reset Link**.
4. Follow the instructions sent to your email.

---

# 📝 How To Use

### Step 1: Login
Create an account or sign in using Firebase Authentication.

### Step 2: Upload Resume
Upload your resume in PDF format.

Supported format:

- PDF (.pdf)

### Step 3: Resume Processing
SkillMap AI automatically:

- Extracts resume text
- Identifies technical skills
- Evaluates resume quality
- Calculates ATS compatibility

### Step 4: Review Analysis

Explore:

- Dashboard
- Resume Analysis
- ATS Analysis
- Learning Plan
- Skill Roadmap
- Course Recommendations
- Resume Suggestions

### Step 5: Improve Your Profile

Use the generated recommendations to:

- Increase ATS score
- Close skill gaps
- Build a learning roadmap
- Prepare for target job roles

---

# 🌟 Features

### 📄 Resume Analysis
- PDF Resume Upload
- Resume Text Extraction
- Resume Quality Assessment
- Resume Insights Generation

### 🎯 ATS Analysis
- ATS Score Calculation
- Keyword Optimization Suggestions
- Resume Improvement Recommendations
- ATS Compatibility Evaluation

### 🧠 Skill Gap Intelligence
- Skill Identification
- Missing Skill Detection
- Gap Analysis
- Career Readiness Evaluation

### 🛣 Learning Roadmap Generator
- Personalized Learning Paths
- Structured Skill Development
- Career Progress Tracking

### 📚 Course Recommendations
- Skill-Based Course Suggestions
- Learning Resource Recommendations
- Career-Oriented Upskilling Guidance

### 🔐 Authentication System
- Firebase Authentication
- Login & Signup
- Password Reset
- Secure Session Management

### ☁ Cloud Deployment
- Streamlit Cloud Hosting
- PostgreSQL Database Integration
- Firebase Backend Services

---

# 🏗 Tech Stack

### Frontend
- Streamlit
- HTML
- CSS
- Plotly

### Backend
- Python

### Database
- PostgreSQL (Neon)

### Authentication
- Firebase Authentication

### Libraries & Tools
- SQLAlchemy
- Pandas
- PyMuPDF
- Plotly
- ReportLab
- Requests
- Python Dotenv

---

# 📂 Project Structure

```text
SkillMapAI/
│
├── frontend/
│   ├── app.py
│   ├── auth.py
│   └── firebase_config.py
│
├── services/
│   ├── ats_scorer.py
│   ├── course_recommender.py
│   ├── database_service.py
│   ├── firebase_service.py
│   ├── learning_recommender.py
│   ├── resume_parser.py
│   ├── roadmap_generator.py
│   └── skill_extractor.py
│
├── database/
│   ├── create_tables.py
│   ├── db_config.py
│   └── schema.sql
│
├── datasets/
│
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙ Installation

### Clone Repository

```bash
git clone https://github.com/aviralsingh06/skillmapAI.git
cd skillmapAI
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔥 Firebase Setup

Create a Firebase Project and enable:

- Authentication
- Email/Password Login

Add the following credentials:

```env
FIREBASE_API_KEY=
FIREBASE_PROJECT_ID=
FIREBASE_AUTH_DOMAIN=
FIREBASE_STORAGE_BUCKET=
```

Place:

```text
firebase-service-account.json
```

inside the project root directory.

---

# 🗄 Database Setup

Create a PostgreSQL database (Neon recommended).

Configure:

```env
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=
```

Create database tables:

```bash
python database/create_tables.py
```

---

# ▶ Run Application

Start the application locally:

```bash
streamlit run frontend/app.py
```

Application URL:

```text
http://localhost:8501
```


# 🌐 Live Demo

### Application Link

https://skillmapai-aviral.streamlit.app

### Demo Access

- Create your own account using Sign Up.
- No admin credentials required.
- Secure authentication powered by Firebase.

---

# 🎯 Future Enhancements

- AI Resume Rewriter
- Resume vs Job Description Matching
- Job Recommendation Engine
- LinkedIn Profile Analyzer
- AI Career Coach
- Interview Preparation Assistant
- Resume Version History
- Advanced Skill Benchmarking

---

# 👨‍💻 Author

### Aviral Singh

B.Tech CSE (Data Science)

Sapthagiri NPS University

### Connect With Me

**LinkedIn:**  
https://www.linkedin.com/in/aviral-singh-a550a5325/

**GitHub:**  
https://github.com/aviralsingh06

---

## ⭐ Support

If you found this project useful, consider giving it a star on GitHub.

It helps the project reach more students and developers.