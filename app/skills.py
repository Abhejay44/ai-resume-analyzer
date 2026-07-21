import re


SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "JavaScript",
    "HTML",
    "CSS",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "FastAPI",
    "Flask",
    "Django",
    "Streamlit",
    "React",
    "Git",
    "GitHub",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "Google Cloud",
    "Linux",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "OpenCV",
    "Matplotlib",
    "Plotly",
    "Machine Learning",
    "Deep Learning",
    "Natural Language Processing",
    "Computer Vision",
    "Data Engineering",
    "Data Analysis",
    "REST API",
]


def extract_skills(text: str) -> list[str]:
    """
    Find known technical skills mentioned in resume text.

    Args:
        text: Plain text extracted from a resume.

    Returns:
        Alphabetically sorted list of detected skills.
    """

    detected_skills = []

    for skill in SKILLS:
        pattern = rf"(?<!\w){re.escape(skill)}(?!\w)"

        if re.search(pattern, text, flags=re.IGNORECASE):
            detected_skills.append(skill)

    return sorted(detected_skills)