import streamlit as st

st.title("AI Resume Analyzer")
st.write("Upload a resume and compare it with a job description.")

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf"],
)