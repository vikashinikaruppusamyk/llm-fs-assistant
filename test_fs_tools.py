from fs_tools import read_file

result = read_file("resumes/resume_john_doe.txt")
print(result)

print("\n--- Testing missing file ---")
result2 = read_file("resumes/does_not_exist.txt")
print(result2)

print("\n--- Testing PDF ---")
result3 = read_file("resumes/resume_neha_kapoor.pdf")
print(result3)

print("\n--- Testing DOCX ---")
result4 = read_file("resumes/resume_ravi_iyer.docx")
print(result4)

print("\n--- Testing list_files ---")
from fs_tools import list_files

all_files = list_files("resumes")
print(all_files)

print("\n--- Testing list_files with extension filter ---")
pdf_only = list_files("resumes", extension=".pdf")
print(pdf_only)

print("\n--- Testing write_file ---")
from fs_tools import write_file

result5 = write_file("output/summary_john_doe.txt", "This is a test summary for John Doe's resume.")
print(result5)

print("\n--- Testing search_in_file ---")
from fs_tools import search_in_file

result6 = search_in_file("resumes/resume_john_doe.txt", "python")
print(result6)