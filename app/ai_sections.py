import json

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def extract_sections_with_ai(
    resume_text: str,
) -> dict[str, str]:
    """
    Use AI to identify resume sections when deterministic
    section detection does not work.
    """

    prompt = f"""
Analyze the resume below and divide it into these sections:

- summary
- education
- experience
- projects
- skills
- certifications
- other

Return ONLY valid JSON.

Use exactly this structure:

{{
    "summary": "",
    "education": "",
    "experience": "",
    "projects": "",
    "skills": "",
    "certifications": "",
    "other": ""
}}

If a section does not exist, use an empty string.

Resume:

{resume_text}
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt,
    )

    ai_text = response.output_text

    sections = json.loads(ai_text)

    return {
        section_name: section_text
        for section_name, section_text in sections.items()
        if section_text.strip()
    }