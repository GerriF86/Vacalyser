import streamlit as st
from utils import *
from config import *

def main():
    st.header("Summary")
    company_name = st.session_state.get("company_info", {}).get("Company Name", "the company")
    st.subheader("Company Information")
    st.write(f"**Company Name:** {st.session_state.company_info.get('Company Name', 'N/A')}")
    st.write(f"**Industry:** {st.session_state.company_info.get('Industry', 'N/A')}")
    st.write(f"**Location:** {st.session_state.company_info.get('Company Location', 'N/A')}")
    st.write(f"**Company Size:** {st.session_state.company_info.get('Company Size', 'N/A')}")
    st.write(f"**Number of Employees:** {st.session_state.company_info.get('Number of Employees', 'N/A')}")
    st.write(
        f"**Number of Employees in the Department:** {st.session_state.company_info.get('Department Employees', 'N/A')}"
    )
    st.write(f"**Website:** {st.session_state.company_info.get('Website', 'N/A')}")
    st.subheader("Job Details")
    st.write(f"**Title:** {st.session_state.role_info.get('job_title', 'N/A')} at {company_name}")
    st.write(f"**Location:** {st.session_state.role_info.get('location', 'N/A')}")
    st.write(
        f"**Work Arrangement:** {st.session_state.role_info.get('work_arrangement', 'N/A')}"
    )
    st.write(
        f"**Work Model:** {st.session_state.role_info.get('onsite_remote_hybrid', 'N/A')}"
    )
    if st.session_state.role_info.get("onsite_remote_hybrid") == "Hybrid":
        st.write(
            f"**Onsite Percentage:** {st.session_state.role_info.get('onsite_percentage', 'N/A')}%"
        )
    st.write(f"**Salary Range:** {st.session_state.role_info.get('salary_range', 'N/A')}")
    st.write(f"**Department:** {st.session_state.role_info.get('department', 'N/A')}")
    st.write(
        f"**Responsible for Money:** {st.session_state.role_info.get('responsible_money', 'N/A')}"
    )
    st.write(
        f"**Responsible for Authority:** {st.session_state.role_info.get('responsible_authority', 'N/A')}"
    )
    st.write(
        f"**Responsible for Need:** {st.session_state.role_info.get('responsible_need', 'N/A')}"
    )
    st.subheader("Tasks")
    if st.session_state.selected_tasks:
        for task in st.session_state.selected_tasks:
            frequency = st.session_state.task_frequencies.get(task, "N/A")
            st.write(f"- {task} (Frequency: {frequency})")
    else:
        st.write("No tasks selected.")
    st.subheader("Skills")
    if st.session_state.selected_must_have_technical_skills or st.session_state.selected_nice_to_have_technical_skills:
        st.write("**Technical Skills:**")
        if st.session_state.selected_must_have_technical_skills:
            st.write("*Must-have:*")
            for skill in st.session_state.selected_must_have_technical_skills:
                st.write(f"   - {skill}")
        if st.session_state.selected_nice_to_have_technical_skills:
            st.write("*Nice-to-have:*")
            for skill in st.session_state.selected_nice_to_have_technical_skills:
                st.write(f"   - {skill}")
    else:
        st.write("No technical skills generated yet.")
    if st.session_state.selected_must_have_soft_skills or st.session_state.selected_nice_to_have_soft_skills:
        st.write("**Soft Skills:**")
        if st.session_state.selected_must_have_soft_skills:
            st.write("*Must-have:*")
            for skill in st.session_state.selected_must_have_soft_skills:
                st.write(f"   - {skill}")
        if st.session_state.selected_nice_to_have_soft_skills:
            st.write("*Nice-to-have:*")
            for skill in st.session_state.selected_nice_to_have_soft_skills:
                st.write(f"   - {skill}")
    else:
        st.write("No soft skills generated yet.")
    st.subheader("Benefits")
    if st.session_state.selected_benefits:
        for benefit in st.session_state.selected_benefits:
            st.write(f"- {benefit}")
    else:
        st.write("No benefits selected.")
    st.subheader("Recruitment Process")
    if st.session_state.selected_steps:
        for step in st.session_state.selected_steps:
            st.write(f"- {step}")
    else:
        st.write("No recruitment steps defined.")
    # --- Hier die neuen Buttons einfügen ---
    st.subheader("Additional Tools")
    job_title = st.session_state.role_info.get("job_title", "")
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
                department = st.session_state.role_info.get("department", "")
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
    # --- Ende der neuen Buttons ---
    # Diversitäts- und Inklusions-Check
    if st.button("Check Diversity and Inclusion"):
        with st.spinner("Checking diversity and inclusion..."):
            job_ad = generate_job_ad(
                st.session_state.role_info,
                st.session_state.company_info,
                st.session_state.selected_benefits,
                st.session_state.selected_steps,
            )
            di_check_result = check_diversity_inclusion(job_ad)
            st.session_state.di_check_result = di_check_result
    # Rechtliche Prüfung
    if st.button("Check Legal Compliance"):
        with st.spinner("Checking legal compliance..."):
            job_ad = generate_job_ad(
                st.session_state.role_info,
                st.session_state.company_info,
                st.session_state.selected_benefits,
                st.session_state.selected_steps,
            )
            legal_check_result = check_legal_compliance(job_ad)
            st.session_state.legal_check_result = legal_check_result
    # Anzeigen der Ergebnisse der Checks
    if "di_check_result" in st.session_state:
        with st.expander("Diversity and Inclusion Check Result", expanded=True):
            st.write(st.session_state.di_check_result)
    if "legal_check_result" in st.session_state:
        with st.expander("Legal Compliance Check Result", expanded=True):
            st.write(st.session_state.legal_check_result)
    
    if st.button("Generate Job Ad"):
        with st.spinner("Generating job advertisement..."):
            job_ad = generate_job_ad(
                st.session_state.role_info,
                st.session_state.company_info,
                st.session_state.selected_benefits,
                st.session_state.selected_steps,
            )
            st.session_state.job_ad = job_ad

    # Download-Buttons für die Berichte
    if "job_ad" in st.session_state:
        st.subheader("Job Advertisement")
        st.text_area("Generated Job Advertisement", st.session_state.job_ad, height=300)
        # Funktion zum Generieren eines Berichts
        def generate_report(job_title, content):
            return f"# Report for {job_title}\n\n{content}"
        # Download-Button für Stellenanzeige
        st.download_button(
            label="Download Job Ad",
            data=generate_report(st.session_state.role_info.get("job_title", "Job Ad"), st.session_state.job_ad),
            file_name="job_ad.txt",
            mime="text/plain"
        )
    # Download-Button für Interviewfragen
    if "interview_questions" in st.session_state:
        st.download_button(
            label="Download Interview Questions",
            data=generate_report(st.session_state.role_info.get("job_title", "Interview Questions"), "\n".join(st.session_state.interview_questions)),
            file_name="interview_questions.txt",
            mime="text/plain"
        )
    # Download-Button für Onboarding-Checkliste
    if "onboarding_checklist" in st.session_state:
        st.download_button(
            label="Download Onboarding Checklist",
            data=generate_report(st.session_state.role_info.get("job_title", "Onboarding Checklist"), 
                                 st.session_state.onboarding_checklist),
            file_name="onboarding_checklist.txt",
            mime="text/plain")
    # Download-Button für Retentionsstrategien
    if "retention_strategies" in st.session_state:
        st.download_button(
            label="Download Retention Strategies",
            data=generate_report(st.session_state.role_info.get("job_title", "Retention Strategies"), "\n".join(st.session_state.retention_strategies)),
            file_name="retention_strategies.txt",
            mime="text/plain"
        )
    # Download-Button für Diversitäts- und Inklusions-Check
    if "di_check_result" in st.session_state:
        st.download_button(
            label="Download Diversity and Inclusion Check Result",
            data=generate_report(st.session_state.role_info.get("job_title", "Diversity and Inclusion Check"), st.session_state.di_check_result),
            file_name="diversity_inclusion_check.txt",
            mime="text/plain"
        )
    # Download-Button für rechtliche Prüfung
    if "legal_check_result" in st.session_state:
        st.download_button(
            label="Download Legal Compliance Check Result",
            data=generate_report(st.session_state.role_info.get("job_title", "Legal Compliance Check"), st.session_state.legal_check_result),
            file_name="legal_compliance_check.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()