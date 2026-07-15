from fastapi import FastAPI

app = FastAPI(title="AI Resume Analyzer")


@app.get("/")
def home():
    return {"message": "AI Resume Analyzer API is running"}