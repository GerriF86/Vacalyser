import streamlit as st

# Importiere die Seiten aus dem pages-Ordner
from pages import welcome_page, company_details_page, department_info_page, job_details_page, tasks_page, skills_page, benefits_page, recruitment_process_page, summary_page, about_us_page
from utils import set_bg_hack

# --- Hintergrundbild ---
# WICHTIG: MUSS VOR st.session_state aufgerufen werden!
set_bg_hack('screenshot.png')

# --- Main App Logic ---
# Initialisiere Session-State Variablen
if "page" not in st.session_state:
    st.session_state.page = "welcome_page"
    st.session_state.company_info = {
        "company_name": "",
        "company_location": "",
        "company_size": "",
        "department_employees": 0,
        "industry": "",
        "website": "",
        "company_culture": [],
        "company_description": ""
    }
    st.session_state.job_details = {
        "job_title": "",
        "location": "",
        "work_arrangement": "Full-Time",
        "work_model": "Onsite",
        "onsite_percentage": 100,
        "salary_range": (0, 0),
        "department": "",
        "budget_authority": "",
        "hiring_authority": "",
        "requisition_originator": "",
        "number_of_vacancies": 1,
        "start_date": None,
        "experience_level_min": 0,
        "experience_level_max": 10,
        "required_languages": [],
        "education_level": "None",
        "internal_contact": "",
        "priority": "Low",
        "travel_requirements": "None",
        "training_budget": 0,
        "direct_supervisor": "",
        "team_size": 0,
        "reporting_line": "",
        "vacancy_reason": "New Position",
        "current_recruitment_process": "",
        "competitor_companies": "",
        "department_keywords": "",
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
    st.session_state.selected_recruitment_steps = []
    st.session_state.interview_questions = []
    st.session_state.onboarding_checklist = []
    st.session_state.retention_strategies = []

# --- Sidebar ---
with st.sidebar:
    if st.button("About Us", key="about_us_sidebar"):
        st.session_state.page = "about_us_page"
        st.rerun()

# Seitenaufrufe
if st.session_state.page == "welcome_page":
    welcome_page.main()
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