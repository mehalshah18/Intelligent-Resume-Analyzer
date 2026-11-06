
import re
from modules.skill_extractor import extract_skills


ACTION_WORDS = (
    "developed", "built", "created", "implemented",
    "designed", "engineered", "programmed", "worked",
    "used", "integrated", "applied", "automated",
    "analyzed", "deployed", "configured"
)


def extract_projects(resume_text):
    """
    Extract multiple projects and their technical skills
    from the Projects section of a resume.
    """

    if not resume_text:
        return []

    text = resume_text.replace("\r", "\n")

    start_match = re.search(
        r"\bprojects?\b\s*[:\-]?\s*",
        text,
        re.IGNORECASE
    )

    if not start_match:
        return []

    project_text = text[start_match.end():]

    end_pattern = (
        r"\b(education|work experience|professional experience|"
        r"experience|technical skills|skills|certifications|"
        r"achievements|qualifications|personal details)\b\s*[:\-]?"
    )

    end_match = re.search(
        end_pattern,
        project_text,
        re.IGNORECASE
    )

    if end_match:
        project_text = project_text[:end_match.start()]

    lines = [
        line.strip()
        for line in project_text.split("\n")
        if line.strip()
    ]

    if not lines:
        return []

    project_headings = []

    for i, line in enumerate(lines):

        # Identify numbered or bullet-point headings.
        explicit_heading = bool(
            re.match(r"^\s*(?:\d+[.)]\s*|[•●▪◦]\s*)", line)
        )

        clean_line = re.sub(
            r"^\s*(?:\d+[.)]\s*|[•●▪◦]\s*)",
            "",
            line
        ).strip()

        # Ignore lines that begin with action words.
        is_action = bool(
            re.match(
                r"(?i)^(?:" + "|".join(ACTION_WORDS) + r")\b",
                clean_line
            )
        )

        if is_action:
            continue

        # A normal heading is usually followed by a description.
        next_line = lines[i + 1] if i + 1 < len(lines) else ""

        next_line_clean = re.sub(
            r"^\s*[•●▪◦\-]\s*",
            "",
            next_line
        )

        next_is_action = bool(
            re.match(
                r"(?i)^(?:" + "|".join(ACTION_WORDS) + r")\b",
                next_line_clean
            )
        )

        if (
            explicit_heading
            or (
                len(clean_line) <= 100
                and not re.search(r"[.!?]$", clean_line)
                and next_is_action
            )
        ):
            project_headings.append((i, clean_line))

    projects = []

    if not project_headings:
        # Fallback: treat the complete section as one project.
        project_headings = [(0, None)]

    for index, (start, name) in enumerate(project_headings):

        if index + 1 < len(project_headings):
            end = project_headings[index + 1][0]
        else:
            end = len(lines)

        description_lines = lines[start + 1:end]

        if name is None:
            description_lines = lines[start:]
            project_text = " ".join(description_lines)

            name = re.split(
                r"\s+(?:developed|built|created|implemented)\b"
                r"|\.\s+|\s+using\s+",
                project_text,
                maxsplit=1,
                flags=re.IGNORECASE
            )[0].strip(" :-,")

        else:
            project_text = " ".join(description_lines)

        skills_data = extract_skills(
            name + " " + project_text
        ) or []

        skill_names = [
            skill["name"]
            for skill in skills_data
            if isinstance(skill, dict) and skill.get("name")
        ]

        if name:
            projects.append({
                "name": name,
                "skills": list(dict.fromkeys(skill_names))
            })

    return projects
