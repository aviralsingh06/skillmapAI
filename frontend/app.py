import streamlit as st
from services.resume_parser import extract_resume_text
from services.database_service import save_resume

st.set_page_config(
    page_title="SkillMap AI",
    page_icon="📊",
    layout="wide"
)

st.title("📊 SkillMap AI")
st.subheader("Resume Skills Gap Analyzer")

uploaded_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)

if uploaded_file is not None:

    extracted_text = extract_resume_text(uploaded_file)

    save_resume(
        uploaded_file.name,
        extracted_text
    )

    st.success("✅ Resume uploaded and saved!")

    st.subheader("Extracted Resume Text")

    st.text_area(
        "Resume Content",
        extracted_text,
        height=300
    )