from fpdf import FPDF

resume_text = """Neha Kapoor
Email: neha.kapoor@email.com
Phone: 555-6789

Summary:
Backend developer with 2 years of experience in Python and Flask.

Skills:
Python, Flask, MongoDB, REST APIs, Git

Experience:
Software Developer, ByteWorks (2023-2025)
- Built REST APIs using Python and Flask
- Worked with MongoDB for data storage
"""

pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", size=12)

for line in resume_text.split("\n"):
    pdf.cell(0, 8, text=line, new_x="LMARGIN", new_y="NEXT")

pdf.output("resumes/resume_neha_kapoor.pdf")
print("PDF created successfully.")