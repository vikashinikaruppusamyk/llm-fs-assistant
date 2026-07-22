from docx import Document

doc = Document()

lines = [
    "Ravi Iyer",
    "Email: ravi.iyer@email.com",
    "Phone: 555-7890",
    "",
    "Summary:",
    "Backend developer with 3 years of experience in Python and FastAPI.",
    "",
    "Skills:",
    "Python, FastAPI, PostgreSQL, Docker, AWS",
    "",
    "Experience:",
    "Software Engineer, NextGen Tech (2022-2025)",
    "- Built REST APIs using Python and FastAPI",
    "- Deployed services on AWS using Docker",
]

for line in lines:
    doc.add_paragraph(line)

doc.save("resumes/resume_ravi_iyer.docx")
print("DOCX created successfully.")