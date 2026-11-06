
import json
import re
from pathlib import Path


# Locate the skills database
BASE_DIR = Path(__file__).resolve().parent.parent
SKILLS_DATABASE = BASE_DIR / "dataset" / "skills.json"


def load_skills():
    """
    Loads skill information from the JSON database.
    """

    with open(SKILLS_DATABASE, "r", encoding="utf-8") as file:
        skills = json.load(file)

    return skills


def extract_skills(text):
    """
    Identifies technical skills present in resume text.
    """

    if not isinstance(text, str):
        raise TypeError("Resume text must be a string.")

    if not text.strip():
        return []

    skills_database = load_skills()

    extracted_skills = []

    # Convert text to lowercase for case-insensitive matching
    resume_text = text.lower()

    for skill in skills_database:

        skill_name = skill["name"]
        aliases = skill["aliases"]

        for alias in aliases:

            # Match complete words or phrases
            pattern = (
                r"(?<![a-zA-Z0-9])"
                + re.escape(alias.lower())
                + r"(?![a-zA-Z0-9])"
            )

            if re.search(pattern, resume_text):

                extracted_skills.append({
                    "name": skill_name,
                    "category": skill["category"]
                })

                # Avoid duplicate entries for the same skill
                break

    return extracted_skills


def get_skills_by_category(extracted_skills):
    """
    Groups extracted skills according to their categories.
    """

    categorized_skills = {}

    for skill in extracted_skills:

        category = skill["category"]
        name = skill["name"]

        if category not in categorized_skills:
            categorized_skills[category] = []

        categorized_skills[category].append(name)

    return categorized_skills
