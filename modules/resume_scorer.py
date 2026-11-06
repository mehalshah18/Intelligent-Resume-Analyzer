
import re

from modules.skill_extractor import load_skills


# =====================================================
# 1. SKILL NORMALIZATION
# =====================================================

def build_skill_alias_map():
    """
    Creates a mapping between skill aliases
    and their standard skill names.
    """

    skills_database = load_skills()

    alias_map = {}

    for skill in skills_database:

        standard_name = skill["name"]

        all_names = skill.get("aliases", []) + [standard_name]

        for alias in all_names:

            alias_map[alias.strip().casefold()] = standard_name

    return alias_map


def normalize_skill_name(skill_name, alias_map):
    """
    Converts a skill name into its standard form.
    """

    normalized_name = skill_name.strip().casefold()

    return alias_map.get(normalized_name, skill_name.strip())


# =====================================================
# 2. SKILL MATCHING SCORE
# =====================================================

def calculate_skill_score(extracted_skills, job_description):
    """
    Calculates matching score for required and preferred skills.
    """

    alias_map = build_skill_alias_map()

    resume_skills = {
        normalize_skill_name(skill["name"], alias_map).casefold()
        for skill in extracted_skills
    }

    required_skills = {
        normalize_skill_name(skill, alias_map).casefold()
        for skill in job_description.get("required_skills", [])
    }

    preferred_skills = {
        normalize_skill_name(skill, alias_map).casefold()
        for skill in job_description.get("preferred_skills", [])
    }

    if not required_skills and not preferred_skills:
        return None

    matched_required = resume_skills & required_skills
    matched_preferred = resume_skills & preferred_skills

    required_score = (
        len(matched_required) / len(required_skills) * 100
        if required_skills else 0
    )

    preferred_score = (
        len(matched_preferred) / len(preferred_skills) * 100
        if preferred_skills else 0
    )

    if required_skills and preferred_skills:

        final_score = (
            required_score * 0.8
            + preferred_score * 0.2
        )

    elif required_skills:
        final_score = required_score

    else:
        final_score = preferred_score

    return round(final_score, 2)


# =====================================================
# 3. JOB REQUIREMENTS SCORE
# =====================================================


def calculate_requirement_score(resume_text, job_description):
    """
    Evaluates required and preferred qualifications
    using phrase variations and common synonyms.
    """

    import re

    required = job_description.get("required_qualifications", [])
    preferred = job_description.get("preferred_qualifications", [])

    if not required and not preferred:
        return None

    text = re.sub(
        r"[^a-z0-9+#]+",
        " ",
        (resume_text or "").lower()
    )
    text = re.sub(r"\s+", " ", text).strip()

    aliases = {
        "communication": [
            "communication",
            "communication skills",
            "verbal communication",
            "written communication",
            "interpersonal communication",
            "effective communicator"
        ],
        "problem solving": [
            "problem solving",
            "problem-solving",
            "analytical thinking",
            "critical thinking",
            "troubleshooting"
        ],
        "teamwork": [
            "teamwork",
            "team work",
            "team player",
            "collaboration",
            "collaborative"
        ],
        "leadership": [
            "leadership",
            "team leader",
            "led a team",
            "team leadership"
        ]
    }

    def qualification_found(qualification):
        qualification = qualification.lower().strip()

        variations = aliases.get(
            qualification,
            [qualification]
        )

        for variation in variations:
            normalized = re.sub(
                r"[^a-z0-9+#]+",
                " ",
                variation.lower()
            )
            normalized = re.sub(
                r"\s+",
                " ",
                normalized
            ).strip()

            if normalized and re.search(
                r"\b" + re.escape(normalized) + r"\b",
                text
            ):
                return True

        return False

    required_matches = sum(
        qualification_found(q) for q in required
    )

    preferred_matches = sum(
        qualification_found(q) for q in preferred
    )

    total_score = 0
    total_weight = 0

    if required:
        total_score += (
            required_matches / len(required)
        ) * 80
        total_weight += 80

    if preferred:
        total_score += (
            preferred_matches / len(preferred)
        ) * 20
        total_weight += 20

    return round(total_score / total_weight * 100, 2)



# =====================================================
# 4. EDUCATION SCORE
# =====================================================

def calculate_education_score(resume_education, job_education):
    """
    Evaluates the candidate's educational qualifications.
    """

    resume_education = resume_education or {}
    job_education = job_education or {}

    required_degree = job_education.get("degree")
    required_fields = job_education.get("fields", [])

    # No education requirements
    if not required_degree and not required_fields:
        return None

    # Initialize ALL score variables before calculations
    total_weight = 0
    earned_score = 0

    # Evaluate degree
    if required_degree:

        total_weight += 60

        resume_degree = resume_education.get("degree") or ""

        if (
            resume_degree.strip().casefold()
            == required_degree.strip().casefold()
        ):
            earned_score += 60

    # Evaluate education field
    if required_fields:

        total_weight += 40

        resume_field = resume_education.get("field") or ""

        if resume_field.casefold() in [
            field.casefold() for field in required_fields
        ]:
            earned_score += 40

    # Prevent division by zero
    if total_weight == 0:
        return None

    final_score = (earned_score / total_weight) * 100

    return round(final_score, 2)


# =====================================================
# 5. EXPERIENCE SCORE
# =====================================================

def calculate_experience_score(resume_experience, job_description):
    """
    Evaluates relevant professional experience.
    """

    resume_experience = resume_experience or {}

    required_years = job_description.get(
        "min_experience_years", 0
    )

    candidate_years = resume_experience.get(
        "years", 0
    )

    if required_years <= 0:
        return None

    score = min(candidate_years / required_years, 1) * 100

    return round(score, 2)


# =====================================================
# 6. PROJECT SCORE
# =====================================================

def calculate_project_score(projects, job_description):
    """
    Evaluates project relevance using normalized skills.
    """

    if not projects:
        return None

    alias_map = build_skill_alias_map()

    required_skills = {
        normalize_skill_name(skill, alias_map).casefold()
        for skill in job_description.get("required_skills", [])
    }

    if not required_skills:
        return None

    project_skills = set()

    for project in projects:

        for skill in project.get("skills", []):

            normalized_skill = normalize_skill_name(
                skill, alias_map
            )

            project_skills.add(normalized_skill.casefold())

    matched_skills = project_skills & required_skills

    score = (
        len(matched_skills) / len(required_skills)
    ) * 100

    return round(score, 2)


# =====================================================
# 7. FINAL SCORE CALCULATION
# =====================================================

def calculate_final_score(
    skill_score,
    requirement_score,
    education_score,
    experience_score,
    project_score
):
    """
    Calculates final score using only available categories.
    """

    weights = {
        "skills": 0.30,
        "requirements": 0.25,
        "education": 0.10,
        "experience": 0.20,
        "projects": 0.15
    }

    scores = {
        "skills": skill_score,
        "requirements": requirement_score,
        "education": education_score,
        "experience": experience_score,
        "projects": project_score
    }

    available_categories = {
        key: score
        for key, score in scores.items()
        if score is not None
    }

    if not available_categories:
        return None

    total_weight = sum(
        weights[key]
        for key in available_categories
    )

    if total_weight == 0:
        return None

    final_score = sum(
        available_categories[key] * weights[key]
        for key in available_categories
    ) / total_weight

    return round(final_score, 2)


# =====================================================
# 8. SCORE EXPLANATION
# =====================================================

def generate_score_explanation(
    extracted_skills,
    job_description,
    individual_scores=None
):
    """
    Generates explanations for resume evaluation.
    """

    alias_map = build_skill_alias_map()

    resume_skills = {
        normalize_skill_name(skill["name"], alias_map).casefold()
        for skill in extracted_skills
    }

    required_skills = {
        normalize_skill_name(skill, alias_map).casefold()
        for skill in job_description.get("required_skills", [])
    }

    preferred_skills = {
        normalize_skill_name(skill, alias_map).casefold()
        for skill in job_description.get("preferred_skills", [])
    }

    matched_required = resume_skills & required_skills
    missing_required = required_skills - resume_skills

    matched_preferred = resume_skills & preferred_skills
    missing_preferred = preferred_skills - resume_skills

    display_names = {
        skill["name"].casefold(): skill["name"]
        for skill in load_skills()
    }

    def display_skills(skills):

        return sorted(
            display_names.get(skill, skill)
            for skill in skills
        )

    explanation = {
        "matched_required_skills": display_skills(matched_required),

        "missing_required_skills": display_skills(missing_required),

        "matched_preferred_skills": display_skills(matched_preferred),

        "missing_preferred_skills": display_skills(missing_preferred),

        "strengths": [],

        "improvements": []
    }

    if matched_required:

        explanation["strengths"].append(
            "Resume contains relevant mandatory technical skills."
        )

    if required_skills and not missing_required:

        explanation["strengths"].append(
            "All mandatory technical skills are present."
        )

    if missing_required:

        explanation["improvements"].append(
            "Missing mandatory skills: "
            + ", ".join(display_skills(missing_required))
        )

    if missing_preferred:

        explanation["improvements"].append(
            "Additional preferred skills to consider: "
            + ", ".join(display_skills(missing_preferred))
        )

    if individual_scores:

        for category, score in individual_scores.items():

            if score is None:
                continue

            if score >= 80:

                explanation["strengths"].append(
                    f"Strong {category} match ({score}%)."
                )

            elif score >= 50:

                explanation["improvements"].append(
                    f"{category.capitalize()} match can be improved ({score}%)."
                )

            else:

                explanation["improvements"].append(
                    f"Low {category} match ({score}%)."
                )

    return explanation


# =====================================================
# 9. MAIN RESUME EVALUATION FUNCTION
# =====================================================

def evaluate_resume(
    resume_text,
    extracted_skills,
    resume_education,
    resume_experience,
    projects,
    job_description
):
    """
    Executes the complete resume scoring system.
    """

    # Calculate individual scores

    skill_score = calculate_skill_score(
        extracted_skills, job_description
    )

    requirement_score = calculate_requirement_score(
        resume_text, job_description
    )

    education_score = calculate_education_score(
        resume_education,
        job_description.get("education", {})
    )

    experience_score = calculate_experience_score(
        resume_experience,
        job_description
    )

    project_score = calculate_project_score(
        projects,
        job_description
    )

    # Calculate overall score

    final_score = calculate_final_score(
        skill_score,
        requirement_score,
        education_score,
        experience_score,
        project_score
    )

    # Collect individual scores

    individual_scores = {
        "skills": skill_score,
        "requirements": requirement_score,
        "education": education_score,
        "experience": experience_score,
        "projects": project_score
    }

    # Generate explanation

    explanation = generate_score_explanation(
        extracted_skills,
        job_description,
        individual_scores
    )

    return {
        "final_score": final_score,
        "individual_scores": individual_scores,
        "explanation": explanation
    }
