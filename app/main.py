from fastapi import FastAPI, File, HTTPException, UploadFile

from app.parser import extract_pdf_text

app = FastAPI(title="AI Resume Analyzer API")


@app.get("/")
def home() -> dict[str, str]:
    """Return a simple health-check message."""

    return {"message": "AI Resume Analyzer API is running"}


@app.post("/upload-resume")
async def upload_resume(
    resume: UploadFile = File(...),
) -> dict[str, str | int]:
    """
    Receive a PDF resume and return extracted text.

    Args:
        resume: PDF file uploaded by the frontend.

    Returns:
        File information and extracted resume text.
    """

    if resume.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
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

    return {
        "filename": resume.filename or "unknown.pdf",
        "content_type": resume.content_type or "unknown",
        "character_count": len(extracted_text),
        "text": extracted_text,
        "message": "Resume text extracted successfully",
    }