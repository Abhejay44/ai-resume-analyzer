from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from app.parser import extract_pdf_text
from app.scorer import calculate_skill_match
from app.skills import extract_skills

app = FastAPI(title="AI Resume Analyzer API")


@app.get("/")
def home() -> dict[str, str]:
    """Return a simple health-check message."""

    return {"message": "AI Resume Analyzer API is running"}


@app.post("/analyze-resume")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
) -> dict[str, object]:
    """
    Compare an uploaded resume with a job description.

    Args:
        resume: PDF resume uploaded by the frontend.
        job_description: Job-description text entered by the user.

    Returns:
        Extracted text, detected skills, and skill-match results.
    """

    if resume.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="The job description cannot be empty.",
        )

    try:
        extracted_text = await extract_pdf_text(resume)
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail="The uploaded PDF could not be processed.",
        ) from error

    if not extracted_text:
        raise HTTPException(
            status_code=400,
            detail="No readable text was found in the PDF.",
        )

    resume_skills = extract_skills(extracted_text)
    job_skills = extract_skills(job_description)

    match_result = calculate_skill_match(
        resume_skills=resume_skills,
        job_skills=job_skills,
    )

    return {
        "filename": resume.filename or "unknown.pdf",
        "character_count": len(extracted_text),
        "text": extracted_text,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "score": match_result["score"],
        "matched_skills": match_result["matched_skills"],
        "missing_skills": match_result["missing_skills"],
        "message": "Resume analysis completed successfully",
    }