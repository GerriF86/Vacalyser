import streamlit as st
from utils import *
from config import *

def main():
    job_title = st.session_state.role_info["job_title"]
    st.subheader("Role Deep Dive", f"Unpacking the {job_title} Position")
    # Extrahiere Infos aus PDF, falls vorhanden
    if "pdf_text" in st.session_state:
        with st.expander("Uploaded Job Description (PDF)", expanded=False):
            st.text_area("Extracted Text", st.session_state.pdf_text, height=300, label_visibility="collapsed")
        # Nutze die extrahierten Infos aus dem PDF für die RAG-Funktionalität
        relevant_docs = [st.session_state.pdf_text]

    # Zwei-Spalten-Layout
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.role_info["Number of Vacancies"] = st.number_input("Number of Vacancies", min_value=1, value=st.session_state.role_info.get("Number of Vacancies", 1))
        st.session_state.role_info["location"] = st.text_input(label="Location", value=st.session_state.role_info.get("location", ""), placeholder="e.g., Berlin, Germany")
        st.session_state.role_info["work_arrangement"] = st.selectbox(
            "Work Arrangement",
            ["Full-Time", "Part-Time", "Contract", "Internship"],
            index=["Full-Time", "Part-Time", "Contract", "Internship"].index(
                st.session_state.role_info.get("work_arrangement", "Full-Time")
            ),
        )
        st.session_state.role_info["onsite_remote_hybrid"] = st.selectbox(
            "Onsite / Remote / Hybrid",
            ["Onsite", "Remote", "Hybrid"],
            index=["Onsite", "Remote", "Hybrid"].index(st.session_state.role_info.get("onsite_remote_hybrid", "Onsite")),
        )
        if st.session_state.role_info["onsite_remote_hybrid"] == "Hybrid":
            st.session_state.role_info["onsite_percentage"] = st.slider(
                "Onsite Percentage", 0, 100, st.session_state.role_info.get("onsite_percentage", 100)
            )
        st.session_state.role_info["department"] = st.text_input("Department", st.session_state.role_info.get("department", ""), placeholder="e.g., Engineering")
        st.session_state.role_info["Start Date"] = st.date_input("Desired Start Date", value=st.session_state.role_info.get("Start Date"))
        
        st.session_state.role_info["level_experience_min"] = st.number_input("Years of Experience (Minimum)", min_value=0, value=st.session_state.role_info.get("level_experience_min",0))
        st.session_state.role_info["level_experience_max"] = st.number_input("Years of Experience (Maximum)", min_value=0, value=st.session_state.role_info.get("level_experience_max", 10))
        st.session_state.role_info["languages"] = st.multiselect("Required Languages", options=["English", "German", "Spanish", "French"], default=st.session_state.role_info.get("languages", []))
        st.session_state.role_info["education_level"] = st.selectbox("Desired Education Level", options=["None", "Bachelor's Degree", "Master's Degree", "PhD"], index= ["None", "Bachelor's Degree", "Master's Degree", "PhD"].index(st.session_state.role_info.get("education_level", "None")))
        st.session_state.role_info["internal_contact_person"] = st.text_input("Internal Contact Person", value=st.session_state.role_info.get("internal_contact_person", ""))
        st.session_state.role_info["direct_supervisor"] = st.text_input("Direct Supervisor", value=st.session_state.role_info.get("direct_supervisor", ""))
        st.session_state.role_info["reporting_line"] = st.text_input("Reporting Line", value=st.session_state.role_info.get("reporting_line", ""))
        st.session_state.role_info["reason_vacancy"] = st.selectbox("Reason for Vacancy", options=["New Position", "Replacement", "Expansion"], index=["New Position", "Replacement", "Expansion"].index(st.session_state.role_info.get("reason_vacancy", "New Position")))
        st.session_state.role_info["current_recruitment_process"] = st.text_area("Current Recruitment Process Description", value=st.session_state.role_info.get("current_recruitment_process", ""))
    with col2:
        st.session_state.role_info["priority"] = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"], index=["Low", "Medium", "High", "Urgent"].index(st.session_state.role_info.get("priority", "Low")))
        st.session_state.role_info["travel_requirements"] = st.selectbox("Travel Requirements", ["None", "Up to 25%", "Up to 50%", "Up to 75%", "More than 75%"], index=["None", "Up to 25%", "Up to 50%", "Up to 75%", "More than 75%"].index(st.session_state.role_info.get("travel_requirements", "None")))
        st.session_state.role_info["training_budget"] = st.number_input("Training Budget per Year (in currency)", min_value=0, value=st.session_state.role_info.get("training_budget", 0))
        st.session_state.role_info["team_size"] = st.number_input("Team Size", min_value=0, value=st.session_state.role_info.get("team_size", 0))
        st.session_state.role_info["competitor_companies"] = st.text_input("Competitor Companies (comma-separated)", value=st.session_state.role_info.get("competitor_companies", ""))
        min_salary, max_salary = st.session_state.role_info.get("salary_range", (0,0))
        if min_salary is None or min_salary < 0 or min_salary > 200000:
            min_salary = 0
        if max_salary is None or max_salary < 0 or max_salary > 200000:
            max_salary = 0
        salary_range = st.slider(
            "Salary Range (in thousands)",
            0,
            200,
            (min_salary, max_salary),
            10,
            format="%d",
        )
        st.session
        st.session_state.role_info["salary_range"] = salary_range
        st.session_state.role_info["responsible_money"] = st.text_input(
            "Budget Authority", value=st.session_state.role_info.get("responsible_money", ""), placeholder="e.g., Department Head"
        )
        st.session_state.role_info["responsible_authority"] = st.text_input(
            "Hiring Authority", value=st.session_state.role_info.get("responsible_authority", ""), placeholder="e.g., Hiring Manager"
        )
        st.session_state.role_info["responsible_need"] = st.text_input(
            "Who defines the need?", value=st.session_state.role_info.get("responsible_need", ""), placeholder="e.g., Team Lead"
        )
        st.session_state.role_info["department_specific_keywords"] = st.text_input("Department-Specific Keywords (comma-separated)", value= st.session_state.role_info.get("department_specific_keywords", ""), placeholder = "e.g., agile, scrum, Kanban")
        st.session_state.role_info["desired_certifications"] = st.multiselect("Desired Certifications", options=["AWS Certified", "Google Cloud Certified", "PMP", "Scrum Master"], default=st.session_state.role_info.get("desired_certifications", []))
        st.session_state.role_info["tools_technologies"] = st.text_area("Specific Tools and Technologies Used (comma-separated)", value=st.session_state.role_info.get("tools_technologies", ""))
        st.session_state.role_info["soft_skills"] = st.text_area("Desired Soft Skills (comma-separated)", value=st.session_state.role_info.get("soft_skills", ""))
    # --- Gehaltsvorschlag ---
        if st.session_state.role_info["location"]:
            with st.expander("Gehaltsvorschlag (geschätzt)"):
                experience_level = st.selectbox("Erfahrungslevel", ["Junior", "Mid-Level", "Senior"])
                experience_years = {"Junior": 1, "Mid-Level": 3, "Senior": 6}.get(experience_level, 1)
                if st.button("Gehaltsspanne schätzen", key="salary_estimate"):
                    with st.spinner("Schätze Gehaltsspanne..."):
                        salary_range = determine_salary(
                            job_title, st.session_state.role_info["location"], experience_years
                        )
                        if salary_range != (None, None):
                            st.write(f"Geschätzte Gehaltsspanne: {salary_range[0]}k - {salary_range[1]}k")
                        else:
                            st.write("Konnte keine Gehaltsspanne schätzen.")
        # --- Ende Gehaltsvorschlag ---
    # --- RAG-Funktionen ---
    if st.button("Generate Job Ad Variations"):
        with st.spinner("Generating job ad variations..."):
            variations = generate_job_ad_variations(
                st.session_state.role_info,
                st.session_state.company_info,
                st.session_state.selected_benefits,
                st.session_state.selected_steps,
                ["general", "tech-savvy", "career starters"],  # Beispielhafte Zielgruppen
                "english",
                ["formal", "informal"]  # Beispielhafte Stile
            )
            st.session_state.job_ad_variations = variations
    if st.button("Suggest Interview Questions"):
        with st.spinner("Generating interview questions..."):
            questions = suggest_interview_questions(
                job_title,
                ["Technical Skills", "Soft Skills", "Company Culture", "Motivation", "Situational Questions"]
            )
            st.session_state.interview_questions = questions
    if st.button("Generate Onboarding Plan"):
        with st.spinner("Generating onboarding plan..."):
            plan = generate_onboarding_plan(
                job_title,
                st.session_state.role_info["department"],
                st.session_state.company_info
            )
            st.session_state.onboarding_plan = plan
    if st.button("Suggest Training Measures"):
        with st.spinner("Suggesting training measures..."):
            training_measures = suggest_training_measures(
                job_title,
                st.session_state.selected_must_have_technical_skills + st.session_state.selected_nice_to_have_technical_skills
            )
            st.session_state.training_measures = training_measures
    if st.button("Analyze Company Culture"):
        with st.spinner("Analyzing company culture..."):
            culture_analysis = analyze_company_culture(
                st.session_state.company_info["Company Name"]
            )
            st.session_state.culture_analysis = culture_analysis
    if st.button("Identify Talent Pools"):
        with st.spinner("Identifying talent pools..."):
            talent_pools = identify_talent_pools(
                job_title,
                st.session_state.selected_must_have_technical_skills + st.session_state.selected_nice_to_have_technical_skills
            )
            st.session_state.talent_pools = talent_pools
    if st.button("Analyze Competitors"):
        with st.spinner("Analyzing competitors..."):
            competitor_analysis = analyze_competitors(
                st.session_state.company_info["Company Name"],
                job_title
            )
            st.session_state.competitor_analysis = competitor_analysis
    if "job_ad_variations" in st.session_state:
        with st.expander("Job Ad Variations"):
            for variation_name, variation_text in st.session_state.job_ad_variations.items():
                st.write(f"**Variation: {variation_name}**")
                st.text_area(f"Job Ad Text", variation_text, height=200, key=f"job_ad_{variation_name}")
    if "interview_questions" in st.session_state:
        with st.expander("Interview Questions"):
            for question in st.session_state.interview_questions:
                st.write(question)
    if "onboarding_plan" in st.session_state:
        with st.expander("Onboarding Plan"):
            st.write(st.session_state.onboarding_plan)
    if "training_measures" in st.session_state:
        with st.expander("Training Measures"):
            st.write(st.session_state.training_measures)
    if "culture_analysis" in st.session_state:
        with st.expander("Company Culture Analysis"):
            st.write(st.session_state.culture_analysis)
    if "talent_pools" in st.session_state:
        with st.expander("Talent Pools"):
            st.write(st.session_state.talent_pools)
    if "competitor_analysis" in st.session_state:
        with st.expander("Competitor Analysis"):
            st.write(st.session_state.competitor_analysis)
    if st.button("Next: Tasks Time"):
        # if "pdf_text" not in st.session_state:
        #     st.session_state.tasks = analyze_role(job_title).get("tasks", [])
        st.session_state.selected_tasks = []
        st.session_state.task_frequencies = {}
        st.session_state.page = "tasks_page"
        st.rerun()

if __name__ == "__main__":
    main()