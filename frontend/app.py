import streamlit as st
from services.resume_parser import extract_resume_text

st.set_page_config(
    page_title="SkillMap AI",
    page_icon="📄",
    layout="wide"
)

st.title("📊 SkillMap AI")
st.subheader("Resume Skills Gap Analyzer")

uploaded_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)

if uploaded_file is not None:
    st.success("Resume uploaded successfully!")

    extracted_text = extract_resume_text(uploaded_file)

    st.subheader("Extracted Resume Text")

    st.text_area(
        "Resume Content",
        extracted_text,
        height=300
    )