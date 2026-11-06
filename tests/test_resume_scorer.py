
from modules.resume_scorer import evaluate_resume


# Sample resume information
resume_text = """
Experienced Python developer.
Good communication and teamwork skills.
Completed B.Tech in Computer Science.
"""

extracted_skills = [
    {"name": "Python", "category": "Programming Languages"},
    {"name": "Django", "category": "Web Development"},
    {"name": "SQL", "category": "Database"},
    {"name": "Git", "category": "Tools"}
]

resume_education = {
    "degree": "B.Tech",
    "field": "Computer Science"
}

resume_experience = {
    "years": 1
}

projects = [
    {
        "name": "Resume Analyzer",
        "skills": ["Python", "Django", "SQL"]
    }
]

job_description = {
    "required_skills": ["Python", "Django", "SQL", "Git"],
    "preferred_skills": ["Docker", "AWS"],

    "required_qualifications": ["communication"],
    "preferred_qualifications": ["teamwork"],

    "education": {
        "degree": "B.Tech",
        "fields": ["Computer Science", "Information Technology"]
    },

    "min_experience_years": 2
}


# Evaluate the resume
result = evaluate_resume(
    resume_text,
    extracted_skills,
    resume_education,
    resume_experience,
    projects,
    job_description
)


# Display results
print("\nRESUME ANALYSIS REPORT")

print("\nFinal Match Score:",
      result["final_score"], "%")

print("\nIndividual Scores:")

for parameter, score in result["individual_scores"].items():
    print(parameter, ":", score, "%")

print("\nExplanation:")

print(result["explanation"])



from modules.resume_scorer import calculate_skill_score


# Test alias recognition
alias_resume_skills = [
    {"name": "JS", "category": "Programming Languages"},
    {"name": "Python 3", "category": "Programming Languages"}
]

alias_job_description = {
    "required_skills": [
        "JavaScript",
        "Python"
    ],

    "preferred_skills": []
}

alias_score = calculate_skill_score(
    alias_resume_skills,
    alias_job_description
)

print("\nALIAS NORMALIZATION TEST")
print("Skill Match Score:", alias_score, "%")

assert alias_score == 100.0

print("Alias normalization test passed!")



from modules.resume_scorer import (
    calculate_skill_score,
    build_skill_alias_map,
    normalize_skill_name
)


def test_skill_normalization():

    alias_map = build_skill_alias_map()

    test_cases = {
        "JS": "JavaScript",
        "javascript": "JavaScript",
        "Python 3": "Python",
        "CPP": "C++",
        "sklearn": "Scikit-learn",
        "k8s": "Kubernetes",
        "nodejs": "Node.js"
    }

    for input_skill, expected_skill in test_cases.items():

        result = normalize_skill_name(
            input_skill,
            alias_map
        )

        assert result == expected_skill, (
            f"Expected {expected_skill}, got {result}"
        )

    print("All skill normalization tests passed!")


def test_alias_skill_matching():

    resume_skills = [
        {"name": "JS", "category": "Programming Languages"},
        {"name": "Python 3", "category": "Programming Languages"}
    ]

    job_description = {
        "required_skills": ["JavaScript", "Python"],
        "preferred_skills": []
    }

    score = calculate_skill_score(
        resume_skills,
        job_description
    )

    assert score == 100.0

    print("Alias skill matching test passed!")


if __name__ == "__main__":
    test_skill_normalization()
    test_alias_skill_matching()


def test_empty_resume_skills():

    score = calculate_skill_score(
        [],
        {
            "required_skills": ["Python", "Java"],
            "preferred_skills": []
        }
    )

    assert score == 0.0

    print("Empty resume skills test passed!")


def test_no_job_skills():

    score = calculate_skill_score(
        [{"name": "Python", "category": "Programming Languages"}],
        {
            "required_skills": [],
            "preferred_skills": []
        }
    )

    assert score == 0.0

    print("Empty job requirements test passed!")


def test_all_skills_matched():

    score = calculate_skill_score(
        [
            {"name": "Python", "category": "Programming Languages"},
            {"name": "SQL", "category": "Database"}
        ],
        {
            "required_skills": ["Python", "SQL"],
            "preferred_skills": []
        }
    )

    assert score == 100.0

    print("Complete skill matching test passed!")

