import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/analyze-resume"

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
)

st.title("📄 AI Resume Analyzer")
st.write(
    "Upload your resume and compare it with a job description."
)

uploaded_file = st.file_uploader(
    "Choose a PDF resume",
    type=["pdf"],
)

job_description = st.text_area(
    "Paste the job description",
    height=250,
    placeholder="Paste the complete job description here...",
)

if st.button("Analyze Resume"):
    if uploaded_file is None:
        st.warning("Please upload a PDF resume.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:
        upload_payload = {
            "resume": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf",
            )
        }

        form_data = {
            "job_description": job_description,
        }

        try:
            response = requests.post(
                API_URL,
                files=upload_payload,
                data=form_data,
                timeout=30,
            )

            response.raise_for_status()
            result = response.json()

            st.success(result["message"])

            st.metric(
                label="Technical Skill Match",
                value=f"{result['score']}%",
            )

            st.subheader("Matched Skills")

            if result["matched_skills"]:
                st.write(", ".join(result["matched_skills"]))
            else:
                st.info("No matching technical skills were found.")

            st.subheader("Missing Skills")

            if result["missing_skills"]:
                st.write(", ".join(result["missing_skills"]))
            else:
                st.success(
                    "No recognized job skills are missing."
                )

            st.subheader("Skills Detected in Resume")

            if result["resume_skills"]:
                st.write(", ".join(result["resume_skills"]))
            else:
                st.info("No known resume skills were detected.")

            st.subheader("Skills Detected in Job Description")

            if result["job_skills"]:
                st.write(", ".join(result["job_skills"]))
            else:
                st.info(
                    "No known technical skills were detected "
                    "in the job description."
                )

            st.subheader("Extracted Resume Text")

            st.text_area(
                "Resume text",
                value=result["text"],
                height=400,
            )

        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to FastAPI. "
                "Make sure the backend is running."
            )

        except requests.exceptions.RequestException as error:
            st.error(f"Analysis failed: {error}")