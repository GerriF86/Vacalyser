import streamlit as st
from utils import *  # Richtig: Importiere set_bg_hack
from config import *

# Importiere die Seiten aus dem pages-Ordner
from pages import welcome_page, data_extraction_page, company_details_page, job_details_page, tasks_page, skills_page, benefits_page, recruitment_process_page, summary_page, about_us_page


# --- Main App Logic ---
# Initialisiere Session-State Variablen
if "page" not in st.session_state:
    st.session_state.page = "welcome_page"
    st.session_state.company_info = {
        "Company Name": "",
        "Company Location": "",
        "Number of Employees": "",
        "Department Employees": 0,
        "Industry": "",
        "Website": "",
        "Unternehmenskultur": [],
        "company_description": ""
    }
    st.session_state.job_title = ""
    st.session_state.role_info = {
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
        "internal_contact_person": "",
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
        "contract_type": ""}
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

# --- Sidebar ---
# Only put navigation buttons in the sidebar
with st.sidebar:
    if st.button("About Us", key="about_us_sidebar"):
        st.session_state.page = "about_us_page"
        st.rerun()

# Seitenaufrufe
if st.session_state.page == "welcome_page":
    welcome_page.main() # Rufe die main-Funktion der jeweiligen Seite auf
elif st.session_state.page == "data_extraction_page":
    data_extraction_page.main()
elif st.session_state.page == "company_details_page":
    company_details_page.main()
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