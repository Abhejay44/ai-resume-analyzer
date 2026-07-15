from fastapi import FastAPI, File, UploadFile

app = FastAPI(title="AI Resume Analyzer API")


@app.get("/")
def home() -> dict[str, str]:
    return {"message": "AI Resume Analyzer API is running"}


@app.post("/upload-resume")
async def upload_resume(
    resume: UploadFile = File(...),
) -> dict[str, str | int]:
    file_contents = await resume.read()

    return {
        "filename": resume.filename or "unknown.pdf",
        "content_type": resume.content_type or "unknown",
        "size_bytes": len(file_contents),
        "message": "Resume received successfully",
    }