from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import pdfplumber
import re
from docx import Document



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
    "btech",
    "b.tech",
    "be",
    "b.e",
    "bachelor",
    "mtech",
    "m.tech",
    "me",
    "m.e",
    "master",
    "phd"
]



app = FastAPI(title="Resume Parsing AI Service")

# --------------------------------------------------
# 🔹 TEXT CLEANING FUNCTION
# --------------------------------------------------
def clean_text(text: str) -> str:
    # Remove extra spaces and line breaks
    text = re.sub(r"\s+", " ", text)

    # Remove non-ASCII characters
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    # Convert to lowercase for uniform processing
    text = text.lower()

    return text.strip()


# --------------------------------------------------
# 🔹 SECTION DETECTION FUNCTION
# --------------------------------------------------
def detect_sections(text: str) -> dict:
    sections = {
        "skills": "",
        "experience": "",
        "education": ""
    }

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


def extract_skills(skills_text: str) -> list:
    extracted_skills = []

    for skill in SKILL_SET:
        if skill in skills_text:
            extracted_skills.append(skill)

    return list(set(extracted_skills))


def extract_experience(experience_text: str) -> dict:
    experience_data = {
        "years": None,
        "roles": []
    }

    # 🔹 Extract years of experience using regex
    years_match = re.search(r"(\d+)\s+years", experience_text)
    if years_match:
        experience_data["years"] = int(years_match.group(1))

    # 🔹 Extract job roles
    for role in JOB_TITLES:
        if role in experience_text:
            experience_data["roles"].append(role)

    experience_data["roles"] = list(set(experience_data["roles"]))

    return experience_data


def extract_education(education_text: str) -> dict:
    education_data = {
        "degree": None,
        "field": None
    }

    # 🔹 Detect degree
    for degree in DEGREES:
        if degree in education_text:
            education_data["degree"] = degree
            break

    # 🔹 Detect field of study
    if "computer science" in education_text:
        education_data["field"] = "computer science"
    elif "information technology" in education_text:
        education_data["field"] = "information technology"
    elif "electronics" in education_text:
        education_data["field"] = "electronics"

    return education_data


def extract_text_from_docx(file) -> str:
    text = ""
    document = Document(file)

    for para in document.paragraphs:
        if para.text:
            text += para.text + "\n"

    return text



# --------------------------------------------------
# 🔹 HEALTH CHECK
# --------------------------------------------------
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "AI service running"
    }


# --------------------------------------------------
# 🔹 PARSE RESUME ENDPOINT (STEP 4.4)
# --------------------------------------------------
@app.post("/parse")
async def parse_resume(file: UploadFile = File(...)):

    # 1️⃣ Validate file
    if not file:
        return JSONResponse(
            status_code=400,
            content={"message": "No file received"}
        )

    # 2️⃣ Only allow PDF for now
    if file.content_type != "application/pdf":
        return JSONResponse(
            status_code=400,
            content={"message": "Only PDF files are supported right now"}
        )

    # 3️⃣ Extract raw text from PDF
    extracted_text = ""

    try:
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text + "\n"
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while reading PDF"}
        )

    # 4️⃣ Check if text extraction failed
    if not extracted_text.strip():
        return JSONResponse(
            status_code=400,
            content={"message": "Could not extract text from PDF"}
        )

    # 5️⃣ STEP 4.4 — CLEAN TEXT
    cleaned_text = clean_text(extracted_text)

    # 6️⃣ STEP 4.4 — DETECT SECTIONS
    sections = detect_sections(cleaned_text)

    # 🔹 Skills
    skills_text = sections.get("skills", "")
    extracted_skills = extract_skills(skills_text)
    
    # 🔹 Experience
    experience_text = sections.get("experience", "")
    experience_data = extract_experience(experience_text)

    # 🔹 Education
    education_text = sections.get("education", "")
    education_data = extract_education(education_text)

    return {
    "filename": file.filename,
    "skills_extracted": extracted_skills,
    "experience": experience_data,
    "education": education_data
    }
