import streamlit as st
from utils import navigate_to_page

def main():
    st.header("Review and Edit Extracted Data")
    if "pdf_text" in st.session_state:
        st.subheader("Data Extracted from PDF")
        # Example for job_title
        st.session_state.role_info["job_title"] = st.text_input("Job Title", value=st.session_state.role_info.get("job_title", ""), key="job_title_extracted")
        # Example for location
        st.session_state.role_info["location"] = st.text_input("Location", value=st.session_state.role_info.get("location", ""), key="location_extracted")
        # Example for tasks
        st.session_state.tasks = st.text_area("Tasks", value="\n".join(st.session_state.tasks), key="tasks_extracted")
        # Example for company name
        st.session_state.company_info["Company Name"] = st.text_input("Company Name", value=st.session_state.company_info.get("Company Name", ""), key="company_name_extracted")
        # Füge alle anderen relevanten Felder hier hinzu, z.B.:
        st.session_state.role_info["contact_person"] = st.text_input("Contact Person", value=st.session_state.role_info.get("contact_person", ""), key="contact_person_extracted")
        st.session_state.role_info["contact_email"] = st.text_input("Contact Email", value=st.session_state.role_info.get("contact_email", ""), key="contact_email_extracted")
        st.session_state.role_info["salary_range"] = st.text_input("Salary Range", value=st.session_state.role_info.get("salary_range", ""), key="salary_range_extracted")
        st.session_state.role_info["contract_type"] = st.text_input("Contract Type", value=st.session_state.role_info.get("contract_type", ""), key="contract_type_extracted")
        st.session_state.benefits = st.text_area("Benefits", value="\n".join(st.session_state.benefits), key="benefits_extracted")
        st.session_state.company_info["company_description"] = st.text_area("Company Description", value=st.session_state.company_info.get("company_description", ""), key="company_description_extracted")
        st.session_state.role_info["required_skills"] = st.text_area("Required Skills", value="\n".join(st.session_state.role_info.get("required_skills", [])), key="required_skills_extracted")
        st.session_state.role_info["Number of Vacancies"] = st.number_input("Number of Vacancies", value=st.session_state.role_info.get("Number of Vacancies", 1), key="vacancies_extracted")
        st.session_state.role_info["Start Date"] = st.date_input("Desired Start Date", value=st.session_state.role_info.get("Start Date"), key="start_date_extracted")
        st.session_state.role_info["department_specific_keywords"] = st.text_input("Department-Specific Keywords", value=st.session_state.role_info.get("department_specific_keywords", ""), key="keywords_extracted")
        st.session_state.role_info["desired_certifications"] = st.text_input("Desired Certifications", value=st.session_state.role_info.get("desired_certifications", ""), key="certifications_extracted")
        st.session_state.role_info["level_experience_min"] = st.number_input("Minimum Years of Experience", value=st.session_state.role_info.get("level_experience_min", 0), key="experience_min_extracted")
        st.session_state.role_info["level_experience_max"] = st.number_input("Maximum Years of Experience", value=st.session_state.role_info.get("level_experience_max", 10), key="experience_max_extracted")
        st.session_state.role_info["languages"] = st.text_input("Required Languages", value=st.session_state.role_info.get("languages", ""), key="languages_extracted")
        st.session_state.role_info["education_level"] = st.text_input("Desired Education Level", value=st.session_state.role_info.get("education_level", ""), key="education_extracted")
        st.session_state.role_info["internal_contact_person"] = st.text_input("Internal Contact Person", value=st.session_state.role_info.get("internal_contact_person", ""), key="internal_contact_extracted")
        st.session_state.role_info["priority"] = st.text_input("Priority of the Position", value=st.session_state.role_info.get("priority", ""), key="priority_extracted")
        st.session_state.role_info["travel_requirements"] = st.text_input("Travel Requirements", value=st.session_state.role_info.get("travel_requirements", ""), key="travel_extracted")
        st.session_state.role_info["training_budget"] = st.number_input("Training Budget", value=st.session_state.role_info.get("training_budget", 0), key="training_budget_extracted")
        st.session_state.role_info["direct_supervisor"] = st.text_input("Direct Supervisor", value=st.session_state.role_info.get("direct_supervisor", ""), key="supervisor_extracted")
        st.session_state.role_info["team_size"] = st.number_input("Team Size", value=st.session_state.role_info.get("team_size", 0), key="team_size_extracted")
        st.session_state.role_info["reporting_line"] = st.text_input("Reporting Line", value=st.session_state.role_info.get("reporting_line", ""), key="reporting_line_extracted")
        st.session_state.role_info["reason_vacancy"] = st.text_input("Reason for Vacancy", value=st.session_state.role_info.get("reason_vacancy", ""), key="reason_extracted")
        st.session_state.role_info["current_recruitment_process"] = st.text_area("Current Recruitment Process Description", value=st.session_state.role_info.get("current_recruitment_process", ""), key="recruitment_process_extracted")
        st.session_state.role_info["competitor_companies"] = st.text_input("Competitor Companies", value=st.session_state.role_info.get("competitor_companies", ""), key="competitors_extracted")
        st.session_state.role_info["tools_technologies"] = st.text_input("Tools and Technologies Used", value=st.session_state.role_info.get("tools_technologies", ""), key="tools_extracted")
        st.session_state.role_info["soft_skills"] = st.text_input("Desired Soft Skills", value=st.session_state.role_info.get("soft_skills", ""), key="soft_skills_extracted")

    
    else:
        st.subheader("Manually Entered Data")
        # Job Title (already entered on welcome_page)
        st.write(f"Job Title: {st.session_state.role_info['job_title']}")
        # Example for location
        st.session_state.role_info["location"] = st.text_input("Location", value=st.session_state.role_info.get("location", ""), key="location_manual")
        # ... (Add fields for other data to be entered manually)
    if st.button("Next"):
        st.session_state.page = "company_details_page"
        st.rerun()

if __name__ == "__main__":
    main()