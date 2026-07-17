import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/upload-resume"

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
)

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume.")

uploaded_file = st.file_uploader(
    "Choose a PDF resume",
    type=["pdf"],
)

if uploaded_file is not None:
    st.write(f"Selected file: {uploaded_file.name}")

    if st.button("Upload Resume"):
        files = {
            "resume": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf",
            )
        }

        try:
            response = requests.post(
                API_URL,
                files=files,
                timeout=30,
            )

            response.raise_for_status()
            result = response.json()

            st.success(result["message"])
            st.write(f"Filename: {result['filename']}")
            st.write(f"Content type: {result['content_type']}")
            st.write(f"Size: {result['size_bytes']} bytes")

        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to FastAPI. "
            )

        except requests.exceptions.RequestException as error:
            st.error(f"Upload failed: {error}")