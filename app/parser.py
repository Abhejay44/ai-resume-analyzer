import fitz
from fastapi import UploadFile


async def extract_pdf_text(resume: UploadFile) -> str:
    """
    Extract plain text from an uploaded PDF.

    Args:
        resume: PDF file received by FastAPI.

    Returns:
        Combined text from every page in the PDF.
    """

    file_contents = await resume.read()

    pdf_document = fitz.open(
        stream=file_contents,
        filetype="pdf",
    )

    page_text = []

    for page in pdf_document:
        page_text.append(page.get_text())

    pdf_document.close()

    return "\n".join(page_text).strip()