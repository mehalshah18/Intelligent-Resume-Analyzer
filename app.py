
import streamlit as st

from modules.resume_parser import extract_text_from_pdf
from modules.text_preprocessing import preprocess_text
from modules.skill_extractor import extract_skills
from modules.resume_scorer import evaluate_resume
from modules.education_extractor import extract_education
from modules.experience_extractor import extract_experience
from modules.project_extractor import extract_projects
from modules.report_generator import generate_pdf_report




# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Intelligent Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# =====================================================
# 2. APPLICATION TITLE
# =====================================================

st.title("📄 Intelligent Resume Analyzer")

st.write(
    "Analyze your resume against a job description "
    "and identify areas for improvement."
)

st.divider()

st.subheader("Welcome!")

st.write(
    """
    This application helps candidates evaluate how well
    their resumes match a particular job description.

    **Features:**
    - Resume PDF upload
    - Job description analysis
    - Technical skill extraction
    - Resume match scoring
    - Identification of missing skills
    - Individual evaluation scores
    """
)

st.divider()


# =====================================================
# 3. INITIALIZE RESUME VARIABLES
# =====================================================

resume_text = ""
extracted_skills = []

resume_education = {
    "degree": "",
    "field": ""
}

resume_experience = {
    "years": 0
}

projects = []


# =====================================================
# 4. RESUME UPLOAD AND PROCESSING
# =====================================================

st.header("1. Upload Your Resume")

uploaded_resume = st.file_uploader(
    "Choose your resume (PDF format)",
    type=["pdf"]
)

if uploaded_resume is not None:

    st.success("Resume uploaded successfully!")

    try:

        # Extract text from PDF
        resume_text = extract_text_from_pdf(uploaded_resume)
        # Extract projects
        projects = extract_projects(resume_text)

        st.subheader("Extracted Projects")

        if projects:
            for project in projects:
                st.write("Project:", project["name"])
                st.write(
                    "Technical Skills:",
                    ", ".join(project["skills"]) or "No skills identified"
        )
        else:
            st.info("No projects found in the resume.")

        # Extract education information
        resume_education = extract_education(resume_text)

        # Extract work experience
        resume_experience = extract_experience(resume_text)

        st.subheader("Extracted Experience Details")
        st.write("Total Experience:", resume_experience["years"], "years")


        st.subheader("Extracted Education Details")

        st.write("Degree:", resume_education["degree"] or "Not found")

        st.write("Education Field:", resume_education["field"] or "Not found")  

        if not resume_text or not resume_text.strip():
            st.error("No readable text found in the uploaded PDF.")

        else:

            st.success("PDF text extraction completed!")

            # Preprocess resume text
            processed_data = preprocess_text(resume_text)

            st.subheader("Preprocessed Resume Text")

            st.text_area(
                "Cleaned Resume Content",
                processed_data["cleaned_text"],
                height=200
            )

            # Extract technical skills
            extracted_skills = extract_skills(resume_text) or []

            st.subheader("Extracted Technical Skills")

            if extracted_skills:

                st.success(
                    f"{len(extracted_skills)} technical skills identified!"
                )

                for skill in extracted_skills:

                    st.write(
                        f"• {skill['name']} ({skill['category']})"
                    )

            else:

                st.warning(
                    "No technical skills were identified."
                )

    except Exception as e:

        st.error(f"Resume processing error: {e}")


st.divider()


# =====================================================
# 5. JOB DESCRIPTION INPUT
# =====================================================

st.header("2. Enter Job Description")

job_title = st.text_input(
    "Job Title",
    placeholder="Example: Python Developer"
)

job_description_text = st.text_area(
    "Paste Job Description",
    placeholder="Enter the complete job description here...",
    height=200
)


# =====================================================
# 6. TECHNICAL SKILL REQUIREMENTS
# =====================================================

st.subheader("Required Technical Skills")

required_skills_input = st.text_input(
    "Mandatory Skills",
    placeholder="Python, SQL, Django, Git"
)

st.subheader("Preferred Technical Skills")

preferred_skills_input = st.text_input(
    "Optional Skills",
    placeholder="AWS, Docker, Kubernetes"
)


# =====================================================
# 7. QUALIFICATION REQUIREMENTS
# =====================================================

st.subheader("Job Qualifications")

required_qualifications_input = st.text_input(
    "Required Qualifications",
    placeholder="Communication, Problem Solving"
)

preferred_qualifications_input = st.text_input(
    "Preferred Qualifications",
    placeholder="Teamwork, Leadership"
)


# =====================================================
# 8. EDUCATION REQUIREMENTS
# =====================================================

st.subheader("Education Requirements")

required_degree = st.selectbox(
    "Required Degree",
    [
        "Not Specified",
        "B.Tech",
        "B.E.",
        "B.Sc.",
        "M.Tech",
        "M.Sc.",
        "MCA"
    ]
)

required_education_field = st.text_input(
    "Required Education Field",
    placeholder="Computer Science, Information Technology"
)


# =====================================================
# 9. EXPERIENCE REQUIREMENTS
# =====================================================

st.subheader("Experience Requirements")

min_experience_years = st.number_input(
    "Minimum Experience (Years)",
    min_value=0,
    max_value=30,
    value=0,
    step=1
)


# =====================================================
# 10. PROCESS JOB DESCRIPTION INPUTS
# =====================================================

required_skills = [
    skill.strip()
    for skill in required_skills_input.split(",")
    if skill.strip()
]

preferred_skills = [
    skill.strip()
    for skill in preferred_skills_input.split(",")
    if skill.strip()
]

required_qualifications = [
    item.strip()
    for item in required_qualifications_input.split(",")
    if item.strip()
]

preferred_qualifications = [
    item.strip()
    for item in preferred_qualifications_input.split(",")
    if item.strip()
]


# =====================================================
# 11. CREATE JOB DESCRIPTION DICTIONARY
# =====================================================

job_description = {

    "job_title": job_title,

    "description": job_description_text,

    "required_skills": required_skills,

    "preferred_skills": preferred_skills,

    "required_qualifications": required_qualifications,

    "preferred_qualifications": preferred_qualifications,

    "education": {

        "degree": (
            None if required_degree == "Not Specified"
            else required_degree
        ),

        "fields": [
            field.strip()
            for field in required_education_field.split(",")
            if field.strip()
        ]

    },

    "min_experience_years": min_experience_years

}


# =====================================================
# 12. RESUME ANALYSIS
# =====================================================

st.divider()

st.header("3. Analyze Resume")

if st.button("Analyze Resume", type="primary"):

    # Validate resume
    if uploaded_resume is None:

        st.error("Please upload your resume first.")

    elif not resume_text.strip():

        st.error(
            "Unable to extract readable text from your resume."
        )

    elif not (
        job_title.strip()
        or job_description_text.strip()
        or required_skills
        or preferred_skills
        or required_qualifications
        or preferred_qualifications
        or required_degree != "Not Specified"
        or required_education_field.strip()
        or min_experience_years > 0
    ):

        st.warning(
            "Please enter some job requirements before analysis."
        )

    else:

        try:

            # Call the resume scoring function
            results = evaluate_resume(

                resume_text,

                extracted_skills,

                resume_education,

                resume_experience,

                projects,

                job_description

            )

            st.success(
                "Resume analysis completed successfully!"
            )

            st.divider()

            # Generate downloadable PDF report
            pdf_report = generate_pdf_report(results, job_title)

            st.download_button(
                label="📥 Download Analysis Report (PDF)",
                data=pdf_report,
                file_name="resume_analysis_report.pdf",
                mime="application/pdf"
            )


            # =================================================
            # 13. DISPLAY FINAL MATCH SCORE
            # =================================================

            st.subheader("Overall Resume Match Score")

            final_score = results["final_score"]

            if final_score is not None:

                st.metric(
                    label="Resume Match",
                    value=f"{final_score}%"
                )

                st.progress(
                    min(100, max(0, int(final_score)))
                )

            else:

                st.warning(
                    "Unable to calculate the final score."
                )


            st.divider()


            # =================================================
            # 14. DISPLAY INDIVIDUAL SCORES
            # =================================================

            st.subheader("Individual Evaluation Scores")

            individual_scores = results["individual_scores"]

            for category, score in individual_scores.items():

                st.write(f"**{category.capitalize()}**")

                if score is not None:

                    st.progress(
                        min(100, max(0, int(score)))
                    )

                    st.write(f"{score}%")

                else:

                    st.info("Not evaluated")


            st.divider()


            # =================================================
            # 15. DISPLAY MATCHED AND MISSING SKILLS
            # =================================================

            explanation = results["explanation"]

            st.subheader("Resume Analysis Details")


            # Matched required skills
            st.write("### Matched Required Skills")

            if explanation["matched_required_skills"]:

                for skill in explanation["matched_required_skills"]:

                    st.write(f"✅ {skill}")

            else:

                st.write("No required skills matched.")


            # Missing required skills
            st.write("### Missing Required Skills")

            if explanation["missing_required_skills"]:

                for skill in explanation["missing_required_skills"]:

                    st.write(f"❌ {skill}")

            else:

                st.write("All required skills are present!")


            # Matched preferred skills
            st.write("### Matched Preferred Skills")

            if explanation["matched_preferred_skills"]:

                for skill in explanation["matched_preferred_skills"]:

                    st.write(f"✅ {skill}")

            else:

                st.write("No preferred skills matched.")


            # Missing preferred skills
            st.write("### Missing Preferred Skills")

            if explanation["missing_preferred_skills"]:

                for skill in explanation["missing_preferred_skills"]:

                    st.write(f"⚠️ {skill}")

            else:

                st.write("No missing preferred skills.")


            st.divider()


            # =================================================
            # 16. DISPLAY STRENGTHS
            # =================================================

            st.subheader("Strengths")

            if explanation["strengths"]:

                for strength in explanation["strengths"]:

                    st.write(f"✅ {strength}")

            else:

                st.write("No specific strengths identified yet.")


            # =================================================
            # 17. DISPLAY AREAS FOR IMPROVEMENT
            # =================================================

            st.subheader("Areas for Improvement")

            if explanation["improvements"]:

                for improvement in explanation["improvements"]:

                    st.write(f"💡 {improvement}")

            else:

                st.write("No specific improvements identified.")


        except Exception as e:

            st.error(
                f"An error occurred during analysis: {e}"
            )


st.divider()

st.caption(
    "Intelligent Resume Analyzer | Resume evaluation system"
)
