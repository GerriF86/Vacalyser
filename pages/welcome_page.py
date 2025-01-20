import streamlit as st
from utils import extract_text_from_pdf_pypdf2, extract_data_from_pdf_rag

def main():
    st.markdown(
        """
        <style>
        .stApp.max-width-0 .main {
            margin-left: 0;
            margin-right: 0;
            padding: 1em;
        }
        .stApp.max-width-0 .main .block-container {
            max-width: 100%;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
        .stApp.max-width-0 .main {
            margin-left: 0;
            margin-right: 0;
            padding: 1em;
        }
        .stApp.max-width-0 .main .block-container {
            max-width: 100%;
        }
        .stApp [data-testid="stText"] {
            text-align: center;
        }
        .stApp [data-testid="stHeader"] {
            visibility: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Willkommensnachricht (zentriert)
    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            <div style='color: #0d47a1; font-size: 4em; font-weight: 900; line-height: 1.2; text-align: center;'>{st.session_state.get('welcome_message', 'Welcome to RecruitSmarts')}</div>
            <div style='color: #0d47a1; font-size: 2.5em; font-weight: 600; line-height: 1.2; text-align: center;'>Revolutionize Your Hiring with AI</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Kurze Beschreibung der App
    st.markdown(
        """
        <p style="font-size: 1.1em; color: #0d47a1; margin-bottom: 1.5em; line-height: 1.6; text-align: center;">
        Stop losing critical information in the early stages of recruitment.
        <b>RecruitSmarts</b> leverages the power of <b>local AI</b> to help you capture every essential detail about your open positions.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # PDF Upload
    uploaded_file = st.file_uploader("Upload a PDF job description", type="pdf")
    if uploaded_file is not None:
        # Extrahieren des Textes
        text = extract_text_from_pdf_pypdf2(uploaded_file)
        if text:
            st.success("PDF uploaded and text extracted successfully!")

            # Daten extrahieren (RAG-basiert)
            extracted_data = extract_data_from_pdf_rag(uploaded_file)

            # Session state aktualisieren
            st.session_state.pdf_text = text
            st.session_state.role_info["job_title"] = extracted_data.get("job_title", "")
            st.session_state.role_info["location"] = extracted_data.get("location", "")
            st.session_state.company_info["Company Name"] = extracted_data.get("company_name", "")
            st.session_state.tasks = extracted_data.get("tasks", [])
            st.session_state.benefits = extracted_data.get("benefits", [])
            st.session_state.company_info["company_description"] = extracted_data.get("company_description", "")
            st.session_state.role_info["required_skills"] = extracted_data.get("required_skills", [])
            st.session_state.role_info["Number of Vacancies"] = extracted_data.get("number_of_vacancies", 1)
            st.session_state.role_info["Start Date"] = extracted_data.get("start_date", None)
            st.session_state.role_info["department_specific_keywords"] = extracted_data.get("department_specific_keywords", "")
            st.session_state.role_info["desired_certifications"] = extracted_data.get("desired_certifications", "")
            st.session_state.role_info["level_experience_min"] = extracted_data.get("level_experience_min", 0)
            st.session_state.role_info["level_experience_max"] = extracted_data.get("level_experience_max", 10)
            st.session_state.role_info["languages"] = extracted_data.get("languages", "")
            st.session_state.role_info["education_level"] = extracted_data.get("education_level", "")
            st.session_state.role_info["internal_contact_person"] = extracted_data.get("internal_contact_person", "")
            st.session_state.role_info["priority"] = extracted_data.get("priority", "")
            st.session_state.role_info["travel_requirements"] = extracted_data.get("travel_requirements", "")
            st.session_state.role_info["training_budget"] = extracted_data.get("training_budget", 0)
            st.session_state.role_info["direct_supervisor"] = extracted_data.get("direct_supervisor", "")
            st.session_state.role_info["team_size"] = extracted_data.get("team_size", 0)
            st.session_state.role_info["reporting_line"] = extracted_data.get("reporting_line", "")
            st.session_state.role_info["reason_vacancy"] = extracted_data.get("reason_vacancy", "")
            st.session_state.role_info["current_recruitment_process"] = extracted_data.get("current_recruitment_process", "")
            st.session_state.role_info["competitor_companies"] = extracted_data.get("competitor_companies", "")
            st.session_state.role_info["tools_technologies"] = extracted_data.get("tools_technologies", "")
            st.session_state.role_info["soft_skills"] = extracted_data.get("soft_skills", "")
            st.session_state.role_info["contract_type"] = extracted_data.get("contract_type", "")
            st.session_state.role_info["salary_range"] = extracted_data.get("salary_range", "")
            st.session_state.role_info["contact_person"] = extracted_data.get("contact_person", "")
            st.session_state.role_info["contact_email"] = extracted_data.get("contact_email", "")

            # Button, um zur nächsten Seite zu navigieren
            if st.button("Proceed to Data Review", key="start_button"):
                navigate_to_page("data_extraction_page")
                st.rerun()
        else:
            st.error("Could not extract text from PDF. Please try another file or use the manual input.")

    # --- MANUELLER INPUT ---
    st.markdown('<p style="font-size: 1.1em; color: #0d47a1; font-weight: 600; margin-bottom: 0.5em; margin-top: 1em; text-align: center;">...or enter job title manually</p>', unsafe_allow_html=True)
    st.session_state.role_info["job_title"] = st.text_input(
        label="Enter Your Vacancy Title to Begin",
        value=st.session_state.role_info.get("job_title", ""),
        placeholder="e.g., Data Scientist, Marketing Guru, Python Developer",
        key="job_title_input",
        label_visibility='collapsed'
    )

    # Button, um zur nächsten Seite zu navigieren (manuelle Eingabe)
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)  # Zentriert den Button
    if st.session_state.role_info["job_title"] and st.button("**Start Building Your Ideal Candidate Profile**", key="start_button_manual"):
        navigate_to_page("data_extraction_page")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()