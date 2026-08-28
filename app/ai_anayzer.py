import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def analyze_resume_with_ai(
    resume_text: str,
    job_description: str,
) -> str:
    """
    Generate resume feedback using OpenAI LLM.

    Args:
        resume_text: Text extracted from the resume.
        job_description: Job description supplied by the user.

    Returns:
        AI-generated resume feedback as text.
    """

    prompt = f"""
You are analyzing a resume against a job description.

Resume:
{resume_text}

Job Description:
{job_description}

Provide concise feedback covering:

1. Professional summary
2. Main strengths
3. Important weaknesses
4. Missing or underemphasized qualifications
5. Specific improvements for this job

Do not invent experience or skills that are not present in the resume.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt,
    )

    return response.output_text