import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/upload-resume"

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
)

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and extract its text.")

uploaded_file = st.file_uploader(
    "Choose a PDF resume",
    type=["pdf"],
)

if uploaded_file is not None:
    st.write(f"Selected file: {uploaded_file.name}")

    if st.button("Extract Resume Text"):
        upload_payload = {
            "resume": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf",
            )
        }

        try:
            response = requests.post(
                API_URL,
                files=upload_payload,
                timeout=30,
            )

            response.raise_for_status()
            result = response.json()

            st.success(result["message"])
            st.write(f"Filename: {result['filename']}")
            st.write(f"Content type: {result['content_type']}")
            st.write(
                f"Extracted characters: "
                f"{result['character_count']}"
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
            st.error(f"Upload failed: {error}")