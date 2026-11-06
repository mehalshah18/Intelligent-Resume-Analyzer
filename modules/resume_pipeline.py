
from modules.resume_parser import extract_text_from_pdf
from modules.text_preprocessing import preprocess_text
from modules.skill_extractor import (
    extract_skills,
    get_skills_by_category
)


def analyze_resume(pdf_file):
    """
    Complete resume analysis pipeline.

    Steps:
    1. Extract text from PDF.
    2. Preprocess extracted text.
    3. Identify technical skills.
    4. Categorize identified skills.
    """

    # Step 1: Extract text from PDF
    extracted_text = extract_text_from_pdf(pdf_file)

    # Step 2: Preprocess extracted text
    preprocessing_result = preprocess_text(extracted_text)

    # Step 3: Use cleaned text for skill extraction
    cleaned_text = preprocessing_result["cleaned_text"]

    extracted_skills = extract_skills(cleaned_text)

    # Step 4: Categorize extracted skills
    categorized_skills = get_skills_by_category(
        extracted_skills
    )

    # Step 5: Return complete analysis results
    return {
        "extracted_text": extracted_text,
        "preprocessing": preprocessing_result,
        "skills": extracted_skills,
        "categorized_skills": categorized_skills
    }
