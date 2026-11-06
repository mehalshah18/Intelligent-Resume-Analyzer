
from modules.resume_parser import extract_text_from_pdf

# Extract text from sample resume
text = extract_text_from_pdf("sample_resume.pdf")

# Display extracted text
print("RESUME TEXT:")
print("-------------------------")
print(text)
