
import re


def extract_education(resume_text):
    """
    Extracts degree and education field from resume text.
    """

    text = resume_text.lower()

    education = {
        "degree": "",
        "field": ""
    }

    # -----------------------------------
    # 1. Extract degree
    # -----------------------------------

    degree_patterns = {
        "B.Tech": r"\bb\.?\s*tech\b|bachelor\s+of\s+technology",
        "B.E.": r"\bb\.?\s*e\.?\b|bachelor\s+of\s+engineering",
        "B.Sc.": r"\bb\.?\s*sc\.?\b|bachelor\s+of\s+science",
        "M.Tech": r"\bm\.?\s*tech\b|master\s+of\s+technology",
        "M.Sc.": r"\bm\.?\s*sc\.?\b|master\s+of\s+science",
        "MCA": r"\bmca\b|master\s+of\s+computer\s+applications"
    }

    for degree, pattern in degree_patterns.items():

        if re.search(pattern, text):
            education["degree"] = degree
            break

    # -----------------------------------
    # 2. Extract education field
    # -----------------------------------

    field_patterns = {
        "Computer Science": [
            r"computer\s+science",
            r"\bcse\b"
        ],

        "Information Technology": [
            r"information\s+technology",
            r"\bit\b"
        ],

        "Electronics": [
            r"electronics",
            r"\bec\b"
        ],

        "Electrical Engineering": [
            r"electrical\s+engineering",
            r"\beee\b"
        ],

        "Mechanical Engineering": [
            r"mechanical\s+engineering"
        ],

        "Civil Engineering": [
            r"civil\s+engineering"
        ],

        "Artificial Intelligence": [
            r"artificial\s+intelligence",
            r"\bai\b"
        ],

        "Data Science": [
            r"data\s+science"
        ]
    }

    for field, patterns in field_patterns.items():

        for pattern in patterns:

            if re.search(pattern, text):

                education["field"] = field
                break

        if education["field"]:
            break

    return education
