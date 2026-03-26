from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import pdfplumber
import re
from docx import Document
import pytesseract
from PIL import Image

# -----------------------------
# 🔹 Skill & Metadata Sets
# -----------------------------

SKILL_SET = [
    "python", "java", "c++", "javascript",
    "react", "node", "express", "mongodb",
    "machine learning", "deep learning", "nlp",
    "data science", "sql", "mysql", "postgresql",
    "docker", "kubernetes", "aws", "git",
    "html", "css", "tailwind", "fastapi"
]

JOB_TITLES = [
    "software engineer",
    "backend developer",
    "frontend developer",
    "full stack developer",
    "data scientist",
    "machine learning engineer",
    "ai engineer",
    "web developer"
]

DEGREES = [
    "btech", "b.tech", "be", "b.e", "bachelor",
    "mtech", "m.tech", "me", "m.e", "master", "phd"
]

app = FastAPI(title="Resume Parsing AI Service")

# -----------------------------
# 🔹 Text Cleaning
# -----------------------------
def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    text = text.lower()
    return text.strip()

# -----------------------------
# 🔹 Section Detection
# -----------------------------
def detect_sections(text: str) -> dict:
    sections = {"skills": "", "experience": "", "education": ""}

    skills_keywords = ["skills", "technical skills", "key skills"]
    experience_keywords = ["experience", "work experience", "professional experience"]
    education_keywords = ["education", "academic background"]

    words = text.split(" ")
    current_section = None

    for word in words:
        if word in skills_keywords:
            current_section = "skills"
            continue
        elif word in experience_keywords:
            current_section = "experience"
            continue
        elif word in education_keywords:
            current_section = "education"
            continue

        if current_section:
            sections[current_section] += word + " "

    return sections

# -----------------------------
# 🔹 Skill Extraction
# -----------------------------
def extract_skills(skills_text: str) -> list:
    extracted = []
    for skill in SKILL_SET:
        if skill in skills_text:
            extracted.append(skill)
    return list(set(extracted))

# -----------------------------
# 🔹 Experience Extraction
# -----------------------------
def extract_experience(experience_text: str) -> dict:
    data = {"years": None, "roles": []}

    years_match = re.search(r"(\d+)\s+years", experience_text)
    if years_match:
        data["years"] = int(years_match.group(1))

    for role in JOB_TITLES:
        if role in experience_text:
            data["roles"].append(role)

    data["roles"] = list(set(data["roles"]))
    return data

# -----------------------------
# 🔹 Education Extraction
# -----------------------------
def extract_education(education_text: str) -> dict:
    data = {"degree": None, "field": None}

    for degree in DEGREES:
        if degree in education_text:
            data["degree"] = degree
            break

    if "computer science" in education_text:
        data["field"] = "computer science"
    elif "information technology" in education_text:
        data["field"] = "information technology"
    elif "electronics" in education_text:
        data["field"] = "electronics"

    return data

# -----------------------------
# 🔹 Format-Specific Extractors
# -----------------------------
def extract_text_from_docx(file) -> str:
    text = ""
    document = Document(file)
    for para in document.paragraphs:
        if para.text:
            text += para.text + "\n"
    return text

def extract_text_from_image(file) -> str:
    image = Image.open(file)
    text = pytesseract.image_to_string(image)
    return text

# -----------------------------
# 🔹 Health Check
# -----------------------------
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "AI service running"}

# -----------------------------
# 🔹 Parse Endpoint
# -----------------------------
@app.post("/parse")
async def parse_resume(file: UploadFile = File(...)):

    if not file:
        return JSONResponse(
            status_code=400,
            content={"message": "No file received"}
        )

    extracted_text = ""

    try:
        # PDF
        if file.content_type == "application/pdf":
            with pdfplumber.open(file.file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        extracted_text += page_text + "\n"

        # DOCX
        elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            extracted_text = extract_text_from_docx(file.file)

        # IMAGE
        elif file.content_type in ["image/jpeg", "image/png"]:
            extracted_text = extract_text_from_image(file.file)

        else:
            return JSONResponse(
                status_code=400,
                content={"message": "Only PDF, DOCX, and image files are supported"}
            )

    except Exception:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while reading resume file"}
        )

    if not extracted_text.strip():
        return JSONResponse(
            status_code=400,
            content={"message": "Could not extract text from resume"}
        )

    cleaned_text = clean_text(extracted_text)
    sections = detect_sections(cleaned_text)

    skills = extract_skills(sections.get("skills", ""))
    experience = extract_experience(sections.get("experience", ""))
    education = extract_education(sections.get("education", ""))

    return {
        "filename": file.filename,
        "skills_extracted": skills,
        "experience": experience,
        "education": education
    }
