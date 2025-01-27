import streamlit as st
from pages.welcome_page import main as welcome_page
from pages.company_details_page import main as company_details_page
from pages.department_info_page import main as department_info_page
from pages.role_info_page import main as role_info_page
from pages.tasks_page import main as tasks_page
from pages.skills_page import main as skills_page
from pages.benefits_page import main as benefits_page
from pages.recruitment_process_page import main as recruitment_process_page
from pages.summary_page import main as summary_page
from core_functions import initialize_rag_chain

# Initialize RAG chain
initialize_rag_chain()

# Use session_state to manage navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'welcome'  # Start on the welcome page

# Mapping of page names to functions
page_map = {
    'welcome': welcome_page,
    'company_details': company_details_page,
    'department_info': department_info_page,
    'role_info': role_info_page,
    'tasks': tasks_page,
    'skills': skills_page,
    'benefits': benefits_page,
    'recruitment_process': recruitment_process_page,
    'summary': summary_page,
}

# Set page config to wide layout
st.set_page_config(layout="wide")

def main():
    # Create tabs
    tabs = st.tabs([
        "Welcome",
        "Company Details",
        "Department Info",
        "Role Info",
        "Tasks",
        "Skills",
        "Benefits",
        "Recruitment Process",
        "Summary"
    ])

    # Tab names corresponding to indices
    tab_names = list(page_map.keys())

    # Update the current page based on session state
    if 'job_details' in st.session_state and st.session_state.job_details and st.session_state.current_page == 'welcome':
        st.session_state.current_page = 'company_details'
    if 'company_info' in st.session_state and st.session_state.company_info and st.session_state.current_page == 'company_details':
        st.session_state.current_page = 'department_info'
    if 'department' in st.session_state and st.session_state.department and st.session_state.current_page == 'department_info':
        st.session_state.current_page = 'role_info'
    if 'job_title' in st.session_state.get('job_details', {}) and st.session_state.job_details['job_title'] and st.session_state.current_page == 'role_info':
        st.session_state.current_page = 'tasks'
    if 'selected_tasks' in st.session_state.get('job_details', {}) and st.session_state.job_details['selected_tasks'] and st.session_state.current_page == 'tasks':
        st.session_state.current_page = 'skills'
    if 'required_skills' in st.session_state.get('job_details', {}) and st.session_state.job_details['required_skills'] and st.session_state.current_page == 'skills':
        st.session_state.current_page = 'benefits'
    if 'selected_benefits' in st.session_state and st.session_state.selected_benefits and st.session_state.current_page == 'benefits':
        st.session_state.current_page = 'recruitment_process'
    if 'selected_recruitment_steps' in st.session_state and st.session_state.selected_recruitment_steps and st.session_state.current_page == 'recruitment_process':
        st.session_state.current_page = 'summary'

    # Determine the current tab index
    current_tab_index = tab_names.index(st.session_state.current_page)

    # Render the corresponding page in its tab
    for i, tab in enumerate(tabs):
        with tab:
            if i == current_tab_index:
                page_map[st.session_state.current_page]()

if __name__ == "__main__":
    main()
