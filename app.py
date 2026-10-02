from flask import Flask, request, render_template
import os
import re

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Basic skills for ResumeIQ
SKILLS = [
    "python",
    "java",
    "javascript",
    "html",
    "css",
    "sql",
    "machine learning",
    "artificial intelligence",
    "data science",
    "flask",
    "django",
    "tensorflow",
    "pandas",
    "numpy",
    "firebase",
    "git",
    "github"
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    resume = request.files.get("resume")
    job_description = request.form.get("job_description", "")

    if not resume:
        return "Please upload a resume."

    # Save resume
    filename = resume.filename
    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    resume.save(file_path)

    # Basic text extraction
    resume_text = ""

    if filename.lower().endswith(".txt"):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            resume_text = file.read()

    elif filename.lower().endswith(".pdf"):
        try:
            import PyPDF2

            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)

                for page in reader.pages:
                    text = page.extract_text()

                    if text:
                        resume_text += text

        except Exception:
            resume_text = ""

    else:
        resume_text = filename

    resume_text = resume_text.lower()
    job_description = job_description.lower()

    # Find skills
    found_skills = []

    for skill in SKILLS:
        if re.search(r"\b" + re.escape(skill) + r"\b", resume_text):
            found_skills.append(skill)

    # Match skills with job description
    required_skills = []

    for skill in SKILLS:
        if re.search(r"\b" + re.escape(skill) + r"\b", job_description):
            required_skills.append(skill)

    matched_skills = [
        skill for skill in required_skills
        if skill in found_skills
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill not in found_skills
    ]

    # Calculate score
    if required_skills:
        score = round(
            (len(matched_skills) / len(required_skills)) * 100
        )
    else:
        score = 0

    return render_template(
        "result.html",
        score=score,
        found_skills=found_skills,
        matched_skills=matched_skills,
        missing_skills=missing_skills
    )


if __name__ == "__main__":
    app.run(debug=True)
