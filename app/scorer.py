def calculate_skill_match(
    resume_skills: list[str],
    job_skills: list[str],
) -> dict[str, int | list[str]]:
    """
    Compare resume skills with job-description skills.

    Args:
        resume_skills: Skills detected in the resume.
        job_skills: Skills detected in the job description.

    Returns:
        Match score, matched skills, and missing skills.
    """

    resume_skill_set = set(resume_skills)
    job_skill_set = set(job_skills)

    matched_skills = sorted(
        resume_skill_set.intersection(job_skill_set)
    )

    missing_skills = sorted(
        job_skill_set.difference(resume_skill_set)
    )

    if not job_skill_set:
        score = 0
    else:
        score = round(
            len(matched_skills) / len(job_skill_set) * 100
        )

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }