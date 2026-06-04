import streamlit as st
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="SkillMap AI",
    page_icon="📊",
    layout="wide"
)

# -------------------------
# Load Environment Variables
# -------------------------
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# -------------------------
# Database Connection
# -------------------------
@st.cache_resource
def connect_db():
    try:
        engine = create_engine(DATABASE_URL)
        return engine
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

engine = connect_db()

# -------------------------
# Header Section
# -------------------------
st.title("📊 SkillMap AI")
st.subheader("AI-Powered Skills Gap & Job Market Analyzer")

st.write("""
Analyze resumes, identify skill gaps, compare skills
with job market trends, and get personalized learning
recommendations.
""")

# -------------------------
# Sidebar Navigation
# -------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Dashboard",
        "Resume Analyzer",
        "Skill Gap Analysis",
        "Job Trends"
    ]
)

# -------------------------
# Database Status Check
# -------------------------
if engine:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        st.success("✅ Database connected successfully!")
    except Exception as e:
        st.error(f"❌ Database Error: {e}")
else:
    st.error("❌ Could not connect to database")

# -------------------------
# Dashboard
# -------------------------
if page == "Dashboard":
    st.header("📈 Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Resumes Analyzed", "0")

    with col2:
        st.metric("Skill Gaps Found", "0")

    with col3:
        st.metric("Job Matches", "0")

    st.info("Upload a resume to begin analysis.")

# -------------------------
# Resume Analyzer
# -------------------------
elif page == "Resume Analyzer":
    st.header("📄 Resume Analyzer")

    uploaded_file = st.file_uploader(
        "Upload Resume (PDF/DOCX)",
        type=["pdf", "docx"]
    )

    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")
        st.info("Resume parsing feature coming next.")

# -------------------------
# Skill Gap Analysis
# -------------------------
elif page == "Skill Gap Analysis":
    st.header("🧠 Skill Gap Analysis")

    target_role = st.selectbox(
        "Select Target Role",
        [
            "Data Analyst",
            "Data Scientist",
            "Machine Learning Engineer",
            "Software Engineer",
            "AI Engineer"
        ]
    )

    st.write(f"Selected Role: **{target_role}**")
    st.info("Skill comparison engine coming next.")

# -------------------------
# Job Trends
# -------------------------
elif page == "Job Trends":
    st.header("📊 Job Market Trends")

    st.info("Live job trend analytics coming soon.")

    sample_data = {
        "Skill": ["Python", "SQL", "Machine Learning"],
        "Demand (%)": [90, 80, 75]
    }

    st.bar_chart(sample_data, x="Skill", y="Demand (%)")