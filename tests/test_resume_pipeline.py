
import unittest
from pathlib import Path

from modules.resume_pipeline import analyze_resume


class TestResumePipeline(unittest.TestCase):

    def setUp(self):

        # Locate the sample PDF in the main project folder
        self.resume_path = (
            Path(__file__).resolve().parent.parent
            / "sample_resume.pdf"
        )

    def test_complete_resume_pipeline(self):

        # Run the complete pipeline
        result = analyze_resume(self.resume_path)

        # Check whether the expected results are returned
        self.assertIn("extracted_text", result)
        self.assertIn("preprocessing", result)
        self.assertIn("skills", result)
        self.assertIn("categorized_skills", result)

        # Check whether PDF text was extracted
        self.assertTrue(result["extracted_text"].strip())

        # Check whether preprocessing returned cleaned text
        self.assertIn(
            "cleaned_text",
            result["preprocessing"]
        )

        # Check whether skills are returned as a list
        self.assertIsInstance(result["skills"], list)

        # Check whether categorized skills are returned as a dictionary
        self.assertIsInstance(
            result["categorized_skills"],
            dict
        )


if __name__ == "__main__":
    unittest.main()
