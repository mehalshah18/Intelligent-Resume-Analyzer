
import re
from datetime import date


MONTHS = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12
}


def extract_experience(resume_text):
    """
    Extract work experience using explicit durations
    and employment date ranges.

    Returns:
        {"years": float}
    """

    if not resume_text:
        return {"years": 0}

    text = re.sub(r"\s+", " ", resume_text.lower())

    start_pattern = (
        r"\b(work experience|professional experience|"
        r"employment history|experience|internships)\b"
    )

    start_match = re.search(start_pattern, text)

    if not start_match:
        return {"years": 0}

    experience_text = text[start_match.end():]

    end_pattern = (
        r"\b(education|academic details|technical skills|"
        r"skills|projects|certifications|achievements|"
        r"personal details|references)\b"
    )

    end_match = re.search(end_pattern, experience_text)

    if end_match:
        experience_text = experience_text[:end_match.start()]

    durations = []

    # Match explicit durations.
    duration_pattern = (
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?"
        r"(?:\s*(?:and)?\s*(\d+)\s*months?)?"
        r"|(\d+)\s*months?"
    )

    matches = re.findall(duration_pattern, experience_text)

    for match in matches:
        if match[0]:
            years = float(match[0])
            months = int(match[1]) if match[1] else 0
            durations.append(years + months / 12)

        elif match[2]:
            durations.append(int(match[2]) / 12)

    # Match month names.
    month_names = "|".join(MONTHS.keys())

    # Supports:
    # Jan 2023 - Dec 2024
    # Jan 2025 - Present
    date_pattern = (
        rf"\b(?P<start_month>{month_names})\.?\s+"
        rf"(?P<start_year>\d{{4}})\s*"
        rf"(?:-|–|—|to|until)\s*"
        rf"(?:(?P<end_month>{month_names})\.?\s+"
        rf"(?P<end_year>\d{{4}})|"
        rf"(?P<current>present|current))\b"
    )

    date_matches = re.finditer(
        date_pattern,
        experience_text
    )

    today = date.today()

    for match in date_matches:

        start_date = date(
            int(match.group("start_year")),
            MONTHS[match.group("start_month")],
            1
        )

        if match.group("current"):
            end_date = date(today.year, today.month, 1)
        else:
            end_date = date(
                int(match.group("end_year")),
                MONTHS[match.group("end_month")],
                1
            )

        if end_date >= start_date:

            # Inclusive month calculation.
            months_worked = (
                (end_date.year - start_date.year) * 12
                + end_date.month - start_date.month
                + 1
            )

            durations.append(months_worked / 12)

    total_experience = max(durations) if durations else 0

    return {"years": round(total_experience, 2)}
