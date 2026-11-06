
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
    page_title="ResumeIQ | Intelligent Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# =====================================================
# 2. CUSTOM WEBSITE DESIGN
# =====================================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #F7F8F4;
}

/* Main content */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* Headings */
h1, h2, h3 {
    color: #24594D !important;
    font-family: 'Segoe UI', sans-serif;
}

/* General text */
p, label {
    color: #40534D;
}

/* Buttons */
.stButton > button {
    background-color: #397B69;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.65rem 1.5rem;
    font-weight: 600;
    transition: 0.2s;
}

.stButton > button:hover {
    background-color: #24594D;
    color: white;
}

/* Input fields */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    border-radius: 10px;
    border: 1px solid #D5E2DA !important;
    background-color: #FFFFFF !important;
    color: #24594D !important;
    -webkit-text-fill-color: #24594D !important;
    font-size: 15px;
}

/* Input placeholders */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder,
.stNumberInput input::placeholder {
    color: #82968B !important;
    -webkit-text-fill-color: #82968B !important;
    opacity: 1 !important;
}

/* Extracted resume text and text areas */
[data-testid="stTextArea"] textarea {
    background-color: #FFFFFF !important;
    color: #24594D !important;
    -webkit-text-fill-color: #24594D !important;
}

/* General displayed text */
.stMarkdown,
.stMarkdown p,
.stMarkdown li,
.stText,
.stCaption {
    color: #40534D;
}

/* Input labels */
.stTextInput label,
.stTextArea label,
.stNumberInput label,
.stSelectbox label {
    color: #24594D !important;
    font-weight: 600;
}

/* Select box text */
.stSelectbox div[data-baseweb="select"] {
    background-color: #FFFFFF;
    color: #24594D;
}

/* Select boxes */
.stSelectbox > div > div {
    border-radius: 10px;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background-color: #EAF2ED;
    border: 2px dashed #8BAF9F;
    border-radius: 15px;
    padding: 15px;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #E1EAE4;
    box-shadow: 0 3px 12px rgba(0,0,0,0.04);
}

/* Progress bar */
.stProgress > div > div > div {
    background-color: #397B69;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #E8F0EA;
}

/* Dividers */
hr {
    border-color: #DCE7DF;
}

/* Section heading cards */
.section-heading {
    background: linear-gradient(120deg, #E8F1EB, #F8EBDD);
    padding: 22px 25px;
    border-radius: 16px;
    margin: 25px 0 18px 0;
    border-left: 5px solid #397B69;
}

.section-heading span {
    color: #397B69;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
}

.section-heading h2 {
    color: #24594D;
    font-size: 24px;
    margin: 8px 0;
}

.section-heading p {
    color: #60766A;
    font-size: 14px;
    margin-bottom: 0;
}

/* Result cards */
.result-card {
    background-color: white;
    border: 1px solid #E1EAE4;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 15px;
}

.result-card h3 {
    margin-top: 0;
}

/* Skill tags */
.skill-tag {
    display: inline-block;
    background-color: #E4F0E9;
    color: #24594D;
    padding: 7px 12px;
    border-radius: 20px;
    margin: 4px;
    font-size: 13px;
    font-weight: 600;
}

.missing-tag {
    display: inline-block;
    background-color: #F8EBDD;
    color: #A45E32;
    padding: 7px 12px;
    border-radius: 20px;
    margin: 4px;
    font-size: 13px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("""
    <div style="text-align:center; padding:15px 5px;">
        <div style="font-size:38px;">📄</div>
        <h2 style="color:#24594D; margin:0;">ResumeIQ</h2>
        <p style="font-size:12px; color:#658276;">
            Intelligent Resume Analyzer
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### ✨ Your Workspace")
    st.markdown("📤 Resume Upload")
    st.markdown("🎯 Job Matching")
    st.markdown("📊 Analysis Results")
    st.markdown("📥 Download Report")

    st.divider()

    st.markdown("### 💡 Quick Tip")
    st.info(
        "Use a clear, updated PDF resume for more accurate analysis."
    )

    st.divider()

    st.caption("ResumeIQ | AI Career Assistant")


# =====================================================
# 4. APPLICATION HEADER
# =====================================================

st.html("""
<div style="
    background: linear-gradient(120deg, #E4F0E9, #F8EBDD);
    padding: 30px;
    border-radius: 20px;
    margin-bottom: 25px;
">
    <div style="font-size:14px; color:#397B69; font-weight:600;">
        ✦ YOUR AI-POWERED CAREER ASSISTANT
    </div>

    <h1 style="font-size:38px; color:#24594D; margin-bottom:8px;">
        Welcome to ResumeIQ
    </h1>

    <p style="font-size:16px; color:#536B60; margin-bottom:0;">
        Analyze your resume, discover skill gaps, and find opportunities
        that match your career goals.
    </p>
</div>
""")

st.write(
    "Your intelligent companion for resume evaluation and career preparation."
)


# =====================================================
# 5. INITIALIZE RESUME VARIABLES
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
# 6. RESUME UPLOAD AND PROCESSING
# =====================================================

st.markdown("""
<div class="section-heading">
    <span>01 · RESUME UPLOAD</span>
    <h2>Let's start with your resume</h2>
    <p>Upload your latest resume in PDF format to begin your analysis.</p>
</div>
""", unsafe_allow_html=True)

uploaded_resume = st.file_uploader(
    "Choose your resume (PDF format)",
    type=["pdf"]
)


if uploaded_resume is not None:

    st.success("Resume uploaded successfully!")

    try:

        # Extract text from PDF
        resume_text = extract_text_from_pdf(uploaded_resume)

        if not resume_text or not resume_text.strip():

            st.error("No readable text found in the uploaded PDF.")

        else:

            st.success("PDF text extraction completed!")

            # Extract projects
            projects = extract_projects(resume_text)

            # Extract education
            resume_education = extract_education(resume_text)

            # Extract experience
            resume_experience = extract_experience(resume_text)

            # Preprocess resume text
            processed_data = preprocess_text(resume_text)

            # Extract technical skills
            extracted_skills = extract_skills(resume_text) or []

            with st.expander("📄 View Extracted Resume Information"):

                st.markdown("### Extracted Projects")

                if projects:

                    for project in projects:

                        st.markdown(
                            f"**{project['name']}**"
                        )

                        st.write(
                            "Technical Skills:",
                            ", ".join(project["skills"])
                            or "No skills identified"
                        )

                else:

                    st.info("No projects found in the resume.")

                st.divider()

                # =========================================
                # EDUCATION DETAILS - VERTICAL ALIGNMENT
                # =========================================

                st.markdown("### Education Details")

                st.markdown(
                    f"**Degree:** {resume_education['degree'] or 'Not found'}"
                )

                st.markdown(
                    f"**Field:** {resume_education['field'] or 'Not found'}"
                )

                st.divider()

                # Experience Details

                st.markdown("### Experience Details")

                st.metric(
                    "Total Experience",
                    f"{resume_experience['years']} years"
                )

                st.divider()

                # Extracted Technical Skills

                st.markdown("### Extracted Technical Skills")

                if extracted_skills:

                    for skill in extracted_skills:

                        st.markdown(
                            f'<span class="skill-tag">'
                            f'{skill["name"]} · {skill["category"]}'
                            f'</span>',
                            unsafe_allow_html=True
                        )

                else:

                    st.warning("No technical skills identified.")

                st.divider()

                # Preprocessed Resume Text

                st.markdown("### Preprocessed Resume Text")

                st.text_area(
                    "Cleaned Resume Content",
                    processed_data["cleaned_text"],
                    height=180
                )

    except Exception as e:

        st.error(f"Resume processing error: {e}")


# =====================================================
# 7. JOB INFORMATION
# =====================================================

st.markdown("""
<div class="section-heading">
    <span>02 · JOB INFORMATION</span>
    <h2>What opportunity are you targeting?</h2>
    <p>Enter the job requirements to evaluate your resume against them.</p>
</div>
""", unsafe_allow_html=True)

job_title = st.text_input(
    "Job Title",
    placeholder="Example: Python Developer"
)

job_description_text = st.text_area(
    "Paste Job Description",
    placeholder="Enter the complete job description here...",
    height=180
)


# =====================================================
# 8. TECHNICAL SKILL REQUIREMENTS
# =====================================================

st.markdown("""
<div class="section-heading">
    <span>03 · SKILL REQUIREMENTS</span>
    <h2>Define your ideal candidate profile</h2>
    <p>Select the skills and qualifications required for this position.</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:

    st.markdown("### Mandatory Skills")

    required_skills_input = st.text_input(
        "Required Technical Skills",
        placeholder="Python, SQL, Django, Git"
    )

with col2:

    st.markdown("### Preferred Skills")

    preferred_skills_input = st.text_input(
        "Optional Technical Skills",
        placeholder="AWS, Docker, Kubernetes"
    )


# =====================================================
# 9. QUALIFICATION REQUIREMENTS
# =====================================================

st.markdown("""
<div class="section-heading">
    <span>04 · QUALIFICATIONS</span>
    <h2>Professional qualifications</h2>
    <p>Add the qualities and abilities expected for this position.</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:

    required_qualifications_input = st.text_input(
        "Required Qualifications",
        placeholder="Communication, Problem Solving"
    )

with col2:

    preferred_qualifications_input = st.text_input(
        "Preferred Qualifications",
        placeholder="Teamwork, Leadership"
    )


# =====================================================
# 10. EDUCATION REQUIREMENTS
# =====================================================

st.markdown("""
<div class="section-heading">
    <span>05 · EDUCATION</span>
    <h2>Academic requirements</h2>
    <p>Specify the degree and education field required for the role.</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:

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

with col2:

    required_education_field = st.text_input(
        "Required Education Field",
        placeholder="Computer Science, Information Technology"
    )


# =====================================================
# 11. EXPERIENCE REQUIREMENTS
# =====================================================

st.markdown("""
<div class="section-heading">
    <span>06 · EXPERIENCE</span>
    <h2>Experience expectations</h2>
    <p>Set the minimum professional experience required.</p>
</div>
""", unsafe_allow_html=True)

min_experience_years = st.number_input(
    "Minimum Experience (Years)",
    min_value=0,
    max_value=30,
    value=0,
    step=1
)


# =====================================================
# 12. PROCESS JOB DESCRIPTION INPUTS
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
# 13. CREATE JOB DESCRIPTION DICTIONARY
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
# 14. RESUME ANALYSIS
# =====================================================

st.markdown("""
<div class="section-heading">
    <span>07 · ANALYSIS</span>
    <h2>Ready to discover your match?</h2>
    <p>Analyze your resume against the job requirements.</p>
</div>
""", unsafe_allow_html=True)

if st.button("✨ Analyze My Resume", type="primary", use_container_width=True):

    # Validate resume
    if uploaded_resume is None:

        st.error("Please upload your resume first.")

    elif not resume_text.strip():

        st.error("Unable to extract readable text from your resume.")

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

        st.warning("Please enter some job requirements before analysis.")

    else:

        try:

            # Call existing resume scoring function
            results = evaluate_resume(
                resume_text,
                extracted_skills,
                resume_education,
                resume_experience,
                projects,
                job_description
            )

            st.success("Resume analysis completed successfully!")

            explanation = results["explanation"]

            # =================================================
            # 15. FINAL MATCH SCORE
            # =================================================

            st.markdown("""
            <div class="section-heading">
                <span>YOUR RESULTS</span>
                <h2>Resume Match Overview</h2>
                <p>See how well your resume matches this opportunity.</p>
            </div>
            """, unsafe_allow_html=True)

            final_score = results["final_score"]

            if final_score is not None:

                score_col1, score_col2 = st.columns([1, 2])

                with score_col1:

                    st.metric(
                        label="Overall Resume Match",
                        value=f"{final_score}%"
                    )

                with score_col2:

                    st.markdown("### Your Compatibility")

                    st.progress(
                        min(100, max(0, int(final_score)))
                    )

                    if final_score >= 80:

                        st.success("Excellent match! Your resume aligns well with this role.")

                    elif final_score >= 60:

                        st.info("Good match! A few improvements may strengthen your application.")

                    else:

                        st.warning("There are skill or qualification gaps to work on.")

            else:

                st.warning("Unable to calculate the final score.")

            # =================================================
            # 16. INDIVIDUAL EVALUATION SCORES
            # =================================================

            st.markdown("### 📊 Individual Evaluation Scores")

            individual_scores = results["individual_scores"]

            score_items = list(individual_scores.items())

            for i in range(0, len(score_items), 2):

                cols = st.columns(2)

                for j, col in enumerate(cols):

                    index = i + j

                    if index < len(score_items):

                        category, score = score_items[index]

                        with col:

                            with st.container(border=True):

                                st.markdown(
                                    f"**{category.capitalize()}**"
                                )

                                if score is not None:

                                    st.progress(
                                        min(100, max(0, int(score)))
                                    )

                                    st.metric(
                                        "Score",
                                        f"{score}%"
                                    )

                                else:

                                    st.info("Not evaluated")

            # =================================================
            # 17. SKILL GAP ANALYSIS
            # =================================================

            st.markdown("""
            <div class="section-heading">
                <span>SKILL GAP ANALYSIS</span>
                <h2>Understand your skill match</h2>
                <p>Identify your existing strengths and missing skills.</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:

                with st.container(border=True):

                    st.markdown("### ✅ Matched Required Skills")

                    if explanation["matched_required_skills"]:

                        for skill in explanation["matched_required_skills"]:

                            st.markdown(
                                f'<span class="skill-tag">{skill}</span>',
                                unsafe_allow_html=True
                            )

                    else:

                        st.write("No required skills matched.")

            with col2:

                with st.container(border=True):

                    st.markdown("### ❌ Missing Required Skills")

                    if explanation["missing_required_skills"]:

                        for skill in explanation["missing_required_skills"]:

                            st.markdown(
                                f'<span class="missing-tag">{skill}</span>',
                                unsafe_allow_html=True
                            )

                    else:

                        st.success("All required skills are present!")

            col1, col2 = st.columns(2)

            with col1:

                with st.container(border=True):

                    st.markdown("### ⭐ Matched Preferred Skills")

                    if explanation["matched_preferred_skills"]:

                        for skill in explanation["matched_preferred_skills"]:

                            st.markdown(
                                f'<span class="skill-tag">{skill}</span>',
                                unsafe_allow_html=True
                            )

                    else:

                        st.write("No preferred skills matched.")

            with col2:

                with st.container(border=True):

                    st.markdown("### ⚠️ Missing Preferred Skills")

                    if explanation["missing_preferred_skills"]:

                        for skill in explanation["missing_preferred_skills"]:

                            st.markdown(
                                f'<span class="missing-tag">{skill}</span>',
                                unsafe_allow_html=True
                            )

                    else:

                        st.success("No missing preferred skills!")

            # =================================================
            # 18. STRENGTHS
            # =================================================

            st.markdown("""
            <div class="section-heading">
                <span>YOUR ADVANTAGES</span>
                <h2>Strengths</h2>
                <p>Discover what makes your resume stand out.</p>
            </div>
            """, unsafe_allow_html=True)

            with st.container(border=True):

                if explanation["strengths"]:

                    for strength in explanation["strengths"]:

                        st.write(f"✅ {strength}")

                else:

                    st.write("No specific strengths identified yet.")

            # =================================================
            # 19. AREAS FOR IMPROVEMENT
            # =================================================

            st.markdown("""
            <div class="section-heading">
                <span>GROWTH OPPORTUNITIES</span>
                <h2>Areas for Improvement</h2>
                <p>Use these suggestions to strengthen your resume.</p>
            </div>
            """, unsafe_allow_html=True)

            with st.container(border=True):

                if explanation["improvements"]:

                    for improvement in explanation["improvements"]:

                        st.write(f"💡 {improvement}")

                else:

                    st.success("No specific improvements identified.")

            # =================================================
            # 20. DOWNLOAD PDF REPORT
            # =================================================

            st.markdown("""
            <div class="section-heading">
                <span>YOUR REPORT</span>
                <h2>Download your analysis</h2>
                <p>Keep a copy of your resume evaluation for future reference.</p>
            </div>
            """, unsafe_allow_html=True)

            pdf_report = generate_pdf_report(results, job_title)

            st.download_button(
                label="📥 Download Analysis Report (PDF)",
                data=pdf_report,
                file_name="resume_analysis_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        except Exception as e:

            st.error(
                f"An error occurred during analysis: {e}"
            )


# =====================================================
# 21. FOOTER
# =====================================================

st.divider()

st.markdown("""
<div style="text-align:center; padding:15px;">
    <p style="color:#658276; font-size:13px;">
        ResumeIQ · Intelligent Resume Analyzer
    </p>
    <p style="color:#8A9B91; font-size:12px;">
        AI-powered resume evaluation and career insights.
    </p>
</div>
""", unsafe_allow_html=True)
