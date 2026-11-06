
import unittest

from modules.skill_extractor import (
    extract_skills,
    get_skills_by_category
)


class TestSkillExtractor(unittest.TestCase):

    def test_basic_skill_extraction(self):

        resume_text = """
        Developed applications using Python, Java,
        C++, SQL, HTML, CSS and JavaScript.
        """

        skills = extract_skills(resume_text)

        skill_names = [skill["name"] for skill in skills]

        self.assertIn("Python", skill_names)
        self.assertIn("Java", skill_names)
        self.assertIn("C++", skill_names)
        self.assertIn("SQL", skill_names)
        self.assertIn("HTML", skill_names)
        self.assertIn("CSS", skill_names)
        self.assertIn("JavaScript", skill_names)

    def test_skill_aliases(self):

        resume_text = """
        Worked with sklearn, ML, cpp and
        cyber security.
        """

        skills = extract_skills(resume_text)

        skill_names = [skill["name"] for skill in skills]

        self.assertIn("Scikit-learn", skill_names)
        self.assertIn("Machine Learning", skill_names)
        self.assertIn("C++", skill_names)
        self.assertIn("Cybersecurity", skill_names)

    def test_empty_resume(self):

        skills = extract_skills("")

        self.assertEqual(skills, [])

    def test_duplicate_skills(self):

        resume_text = """
        Python developer with Python experience.
        Python programming using Python 3.
        """

        skills = extract_skills(resume_text)

        skill_names = [skill["name"] for skill in skills]

        self.assertEqual(skill_names.count("Python"), 1)

    def test_skill_categorization(self):

        resume_text = """
        Python, SQL, HTML and Machine Learning.
        """

        skills = extract_skills(resume_text)

        categorized = get_skills_by_category(skills)

        self.assertIn("Programming Languages", categorized)
        self.assertIn("Database", categorized)
        self.assertIn("Web Development", categorized)
        self.assertIn("Artificial Intelligence", categorized)


if __name__ == "__main__":
    unittest.main()
