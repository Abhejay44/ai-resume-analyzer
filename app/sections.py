import re


SECTION_HEADINGS = {
    "education": [
        "education",
        "academic background",
        "academic qualifications",
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "training / experience",
    ],
    "projects": [
        "projects",
        "project experience",
        "academic projects",
        "projects undertaken",
    ],
    "skills": [
        "skills",
        "technical skills",
        "technologies",
        "core competencies",
    ],
    "certifications": [
        "certifications",
        "certificates",
        "licenses",
    ],
}


def normalize_heading(line: str) -> str:
    """
    Normalize section headings for comparison.

    Args:
        line: One line of resume text.

    Returns:
        Lowercase text with extra symbols and spaces removed.
    """

    normalized_line = line.lower().strip()
    normalized_line = re.sub(r"[_:|\-]+", " ", normalized_line)
    normalized_line = re.sub(r"\s+", " ", normalized_line)

    return normalized_line.strip()


def identify_section(line: str) -> str | None:
    """
    Determine whether a line is a recognized section heading.

    Args:
        line: One line of resume text.

    Returns:
        Standard section name or None when no heading is recognized.
    """

    normalized_line = normalize_heading(line)

    for section_name, possible_headings in SECTION_HEADINGS.items():
        if normalized_line in possible_headings:
            return section_name

    return None


def extract_sections(text: str) -> dict[str, str]:
    """
    Divide resume text into recognized sections.

    Args:
        text: Complete text extracted from a resume.

    Returns:
        Dictionary mapping section names to their text.
    """

    sections: dict[str, list[str]] = {
        "summary": [],
        "education": [],
        "experience": [],
        "projects": [],
        "skills": [],
        "certifications": [],
        "other": [],
    }

    current_section = "summary"

    for line in text.splitlines():
        cleaned_line = line.strip()

        if not cleaned_line:
            continue

        detected_section = identify_section(cleaned_line)

        if detected_section is not None:
            current_section = detected_section
            continue

        sections[current_section].append(cleaned_line)

    return {
        section_name: "\n".join(section_lines)
        for section_name, section_lines in sections.items()
        if section_lines
    }
def section_detection_is_weak(
    sections: dict[str, str],
) -> bool:
    """
    Decide if deterministic section detection is usable or not. (By checking if at least 2 important sections are detected)

    Args:
        sections: Detected resume sections.

    Returns:
        True when too few important sections were detected.
    """

    important_sections = {
        "education",
        "experience",
        "projects",
        "skills",
    }

    detected_important_sections = important_sections.intersection(
        sections.keys()
    )

    return len(detected_important_sections) < 2