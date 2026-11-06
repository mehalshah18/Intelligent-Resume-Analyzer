from modules.resume_scorer import (
    calculate_skill_score,
    calculate_requirement_score,
    calculate_education_score,
    calculate_experience_score,
    calculate_project_score,
    calculate_final_score,
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
        result = normalize_skill_name(input_skill, alias_map)

        assert result == expected_skill, (
            f"Expected {expected_skill}, got {result}"
        )

    print("Skill normalization test passed!")


def test_alias_skill_matching():
    resume_skills = [
        {"name": "JS", "category": "Programming Languages"},
        {"name": "Python 3", "category": "Programming Languages"}
    ]

    job_description = {
        "required_skills": ["JavaScript", "Python"],
        "preferred_skills": []
    }

    score = calculate_skill_score(resume_skills, job_description)

    assert score == 100.0

    print("Alias skill matching test passed!")


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

    assert score is None

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


def test_no_job_qualifications():
    score = calculate_requirement_score(
        "",
        {
            "required_qualifications": [],
            "preferred_qualifications": []
        }
    )

    assert score is None
    print("Missing job qualifications test passed!")


def test_no_job_education():
    score = calculate_education_score(
        {"degree": "B.Tech", "field": "Computer Science"},
        {}
    )

    assert score is None
    print("Missing job education test passed!")


def test_no_experience_requirement():
    score = calculate_experience_score(
        {"years": 1},
        {"min_experience_years": 0}
    )

    assert score is None
    print("Missing experience requirement test passed!")


def test_no_projects():
    score = calculate_project_score(
        [],
        {"required_skills": ["Python", "SQL"]}
    )

    assert score is None
    print("Missing project information test passed!")


def test_final_score_calculation():

    # All categories available
    score = calculate_final_score(
        80, 100, 100, 50, 75
    )

    assert score == 80.25

    # Some categories unavailable
    score = calculate_final_score(
        80, None, 100, None, 75
    )

    assert score == 82.27

    print("Final score calculation tests passed!")


if __name__ == "__main__":

    test_skill_normalization()
    test_alias_skill_matching()
    test_empty_resume_skills()
    test_no_job_skills()
    test_all_skills_matched()

    test_no_job_qualifications()
    test_no_job_education()
    test_no_experience_requirement()
    test_no_projects()

    test_final_score_calculation()

