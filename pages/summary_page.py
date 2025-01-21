import streamlit as st
from utils import *
from pages import *

def main():
    st.header("Summary")
    company_name = st.session_state.company_info.get("company_name", "the company")

    # --- Company Information ---
    st.subheader("Company Information")
    st.write(f"**Company Name:** {st.session_state.company_info.get('company_name', 'N/A')}")
    st.write(f"**Industry:** {st.session_state.company_info.get('industry', 'N/A')}")
    st.write(f"**Location:** {st.session_state.company_info.get('company_location', 'N/A')}")
    st.write(f"**Company Size:** {st.session_state.company_info.get('company_size', 'N/A')}")
    st.write(f"**Department Size:** {st.session_state.company_info.get('department_size', 'N/A')}")
    st.write(f"**Website:** {st.session_state.company_info.get('website', 'N/A')}")
    st.write(f"**Company Culture:** {st.session_state.company_info.get('company_culture', 'N/A')}")
    st.write(f"**Reporting Line:** {st.session_state.job_details.get('reporting_line', 'N/A')}")

    # --- Job Details ---
    st.subheader("Job Details")
    st.write(f"**Title:** {st.session_state.job_details.get('job_title', 'N/A')} at {company_name}")
    st.write(f"**Location:** {st.session_state.job_details.get('job_location', 'N/A')}")
    st.write(f"**Work Arrangement:** {st.session_state.job_details.get('work_arrangement', 'N/A')}")
    st.write(f"**Work Model:** {st.session_state.job_details.get('work_model', 'N/A')}")
    st.write(f"**Onsite Percentage:** {st.session_state.job_details.get('onsite_percentage', 'N/A')}%")
    st.write(f"**Start Date:** {st.session_state.job_details.get('start_date', 'N/A')}")
    st.write(f"**Department:** {st.session_state.job_details.get('department', 'N/A')}")
    st.write(f"**Contract Type:** {st.session_state.job_details.get('contract_type', 'N/A')}")
    st.write(f"**Salary Range:** {st.session_state.job_details.get('salary_range', 'N/A')}")
    st.write(f"**Priority:** {st.session_state.job_details.get('priority', 'N/A')}")
    st.write(f"**Reason for Vacancy:** {st.session_state.job_details.get('vacancy_reason', 'N/A')}")
    st.write(f"**Internal Contact:** {st.session_state.job_details.get('internal_contact', 'N/A')}")
    st.write(f"**Budget Authority:** {st.session_state.job_details.get('budget_authority', 'N/A')}")
    st.write(f"**Contact Email:** {st.session_state.job_details.get('contact_email', 'N/A')}")
    st.write(f"**Hiring Authority:** {st.session_state.job_details.get('hiring_authority', 'N/A')}")
    st.write(f"**Requisition Originator:** {st.session_state.job_details.get('requisition_originator', 'N/A')}")
    st.write(f"**Direct Supervisor:** {st.session_state.job_details.get('direct_supervisor', 'N/A')}")
    st.write(f"**Team Size:** {st.session_state.job_details.get('team_size', 'N/A')}")
    st.write(f"**Training Budget:** {st.session_state.job_details.get('training_budget', 'N/A')}")
    st.write(f"**Travel Requirements:** {st.session_state.job_details.get('travel_requirements', 'N/A')}")

    # --- Tasks ---
    st.subheader("Tasks")
    if st.session_state.selected_tasks:
        for task in st.session_state.selected_tasks:
            frequency = st.session_state.task_frequencies.get(task, "N/A")
            st.write(f"- {task} (Frequency: {frequency})")
    else:
        st.write("No tasks selected.")

    # --- Skills ---
    st.subheader("Skills")
    st.write("**Required Skills:**")
    if st.session_state.job_details.get("required_skills"):
        st.write(st.session_state.job_details.get("required_skills"))
    else:
        st.write("N/A")
    
    st.write(f"**Minimum Experience (Required):** {st.session_state.job_details.get('experience_level_min_req', 'N/A')}")
    st.write(f"**Maximum Experience (Required):** {st.session_state.job_details.get('experience_level_max_req', 'N/A')}")

    st.write("**Technical Skills:**")
    if st.session_state.job_details.get("technical_skills"):
        st.write(st.session_state.job_details.get("technical_skills"))
    else:
        st.write("N/A")

    st.write(f"**Minimum Experience (Technical):** {st.session_state.job_details.get('experience_level_min_tech', 'N/A')}")
    st.write(f"**Maximum Experience (Technical):** {st.session_state.job_details.get('experience_level_max_tech', 'N/A')}")

    st.write("**Desired Certifications:**")
    if st.session_state.job_details.get("desired_certifications"):
        st.write(st.session_state.job_details.get("desired_certifications"))
    else:
        st.write("N/A")

    st.write(f"**Education Level:** {st.session_state.job_details.get('education_level', 'N/A')}")

    st.write("**Soft Skills:**")
    if st.session_state.job_details.get("soft_skills"):
        st.write(st.session_state.job_details.get("soft_skills"))
    else:
        st.write("N/A")

    st.write(f"**Minimum Experience (Soft):** {st.session_state.job_details.get('experience_level_min_soft', 'N/A')}")
    st.write(f"**Maximum Experience (Soft):** {st.session_state.job_details.get('experience_level_max_soft', 'N/A')}")

    st.write("**Required Languages:**")
    if st.session_state.job_details.get("required_languages"):
        st.write(st.session_state.job_details.get("required_languages"))
    else:
        st.write("N/A")

    st.write(f"**Minimum Experience (Languages):** {st.session_state.job_details.get('experience_level_min_lang', 'N/A')}")
    st.write(f"**Maximum Experience (Languages):** {st.session_state.job_details.get('experience_level_max_lang', 'N/A')}")

    # --- Benefits ---
    st.subheader("Benefits")
    if st.session_state.selected_benefits:
        for benefit in st.session_state.selected_benefits:
            st.write(f"- {benefit}")
    else:
        st.write("No benefits selected.")

    # --- Recruitment Process ---
    st.subheader("Recruitment Process")
    st.write(f"**Current Recruitment Process:** {st.session_state.job_details.get('current_recruitment_process', 'N/A')}")
    if st.session_state.selected_recruitment_steps:
        for step in st.session_state.selected_recruitment_steps:
            st.write(f"- {step}")
    else:
        st.write("No recruitment steps defined.")
    
    st.write(f"**Competitor Companies:** {st.session_state.company_info.get('competitor_companies', 'N/A')}")
    st.write(f"**Tools and Technologies:** {st.session_state.job_details.get('tools_technologies', 'N/A')}")

    # --- Additional Tools ---
    st.subheader("Additional Tools")
    job_title = st.session_state.job_details.get("job_title", "")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Prepare Interview Questions", key="prepare_interview"):
            with st.spinner("Generating interview questions..."):
                focus_areas = ["Technical Skills", "Soft Skills", "Company Culture", "Motivation", "Situational Questions"]
                questions = prepare_interview(job_title, focus_areas)
                st.session_state.interview_questions = questions

    with col2:
        if st.button("Create Onboarding Checklist", key="onboarding_checklist"):
            with st.spinner("Generating onboarding checklist..."):
                department = st.session_state.job_details.get("department", "")
                checklist = create_onboarding_checklist(job_title, department)
                st.session_state.onboarding_checklist = checklist

    with col3:
        if st.button("Suggest Retention Strategies", key="retention_strategies"):
            with st.spinner("Generating retention strategies..."):
                strategies = suggest_retention_strategies(job_title)
                st.session_state.retention_strategies = strategies

    # Anzeigen der generierten Inhalte, falls vorhanden
    if "interview_questions" in st.session_state:
        with st.expander("Interview Questions", expanded=True):
            for question in st.session_state.interview_questions:
                st.write(f"- {question}")

    if "onboarding_checklist" in st.session_state:
        with st.expander("Onboarding Checklist", expanded=True):
            for item in st.session_state.onboarding_checklist:
                st.write(f"- {item}")

    if "retention_strategies" in st.session_state:
        with st.expander("Retention Strategies", expanded=True):
            for strategy in st.session_state.retention_strategies:
                st.write(f"- {strategy}")

    if styled_button("Generate Job Ad"):
        with st.spinner("Generating job advertisement..."):
            job_ad = generate_job_ad(
                st.session_state.job_details,
                st.session_state.company_info,
                st.session_state.selected_benefits,
                st.session_state.selected_steps,
            )
            st.subheader("Job Advertisement")
            st.text_area("Generated Job Advertisement", job_ad, height=600, label_visibility="collapsed")

# --- About Us Page ---
def about_us_page():
    st.header("About Us")
    st.markdown(
        """
        <p style="font-size: 1.1em; color: #e6edf3; margin-bottom: 1.5em; line-height: 1.6;">
        RecruitSmarts is an AI-powered talent acquisition app designed to streamline the hiring process.
        </p>
        """,
        unsafe_allow_html=True,
    )

# --- Main App Logic ---
def main():
    # Set the initial page and configure the layout (Configured in config.toml)
    # Page config:
    # st.set_page_config(page_title="Find your perfect candidate", layout="wide", initial_sidebar_state="collapsed")

    # Initialisiere Session-State Variablen
    if "page" not in st.session_state:
        st.session_state.page = "welcome_page"
        st.session_state.company_info = {
            "Company Name": "",
            "Company Location": "",
            "Company Size": "",
            "Department Employees": 0,
            "Industry": "",
            "Website": "",
            "Unternehmenskultur": [],
            "company_description": ""
        }
        st.session_state.job_title = ""
        st.session_state.job_details = {
            "job_title": "",
            "location": "",
            "work_arrangement": "Full-Time",
            "onsite_remote_hybrid": "Onsite",
            "onsite_percentage": 100,
            "salary_range": (0, 0),
            "department": "",
            "responsible_money": "",
            "responsible_authority": "",
            "responsible_need": "",
            "Number of Vacancies": 1,
            "Start Date": None,
            "level_experience_min": 0,
            "level_experience_max": 10,
            "languages": [],
            "education_level": "None",
            "internal_contact": "",
            "priority": "Low",
            "travel_requirements": "None",
            "training_budget": 0,
            "direct_supervisor": "",
            "team_size": 0,
            "reporting_line": "",
            "reason_vacancy": "New Position",
            "current_recruitment_process": "",
            "competitor_companies": "",
            "department_specific_keywords": "",
            "desired_certifications": [],
            "tools_technologies": "",
            "soft_skills": "",
            "required_skills": [],
            "contact_person": "",
            "contact_email": "",
            "contract_type": ""
        }
        st.session_state.tasks = []
        st.session_state.selected_tasks = []
        st.session_state.task_frequencies = {}
        st.session_state.technical_skills = {}
        st.session_state.soft_skills = {}
        st.session_state.selected_must_have_technical_skills = []
        st.session_state.selected_nice_to_have_technical_skills = []
        st.session_state.selected_must_have_soft_skills = []
        st.session_state.selected_nice_to_have_soft_skills = []
        st.session_state.benefits = {}
        st.session_state.selected_benefits = []
        st.session_state.recruitment_process = []
        st.session_state.recruitment_process_steps = []
        st.session_state.selected_steps = []
        st.session_state.company_questions = {}
        st.session_state.interview_questions = []
        st.session_state.onboarding_checklist = []
        st.session_state.retention_strategies = []

    # --- Sidebar ---# Only put navigation buttons in the sidebar
    with st.sidebar:
        if st.button("About Us", key="about_us_sidebar"):
            st.session_state.page = "about_us_page"
            st.rerun()

    # Seitenaufrufe
    if st.session_state.page == "welcome_page":
        welcome_page.main()  # Rufe die main-Funktion der jeweiligen Seite auf
    elif st.session_state.page == "company_details_page":
        company_details_page.main()
    elif st.session_state.page == "department_info_page":
        department_info_page.main()
    elif st.session_state.page == "job_details_page":
        job_details_page.main()
    elif st.session_state.page == "tasks_page":
        tasks_page.main()
    elif st.session_state.page == "skills_page":
        skills_page.main()
    elif st.session_state.page == "benefits_page":
        benefits_page.main()
    elif st.session_state.page == "recruitment_process_page":
        recruitment_process_page.main()
    elif st.session_state.page == "summary_page":
        summary_page.main()
    elif st.session_state.page == "about_us_page":
        about_us_page.main()

if __name__ == "__main__":
    main()