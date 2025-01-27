# pages/5_skills_page.py
import streamlit as st
from ui_elements import (
    centered_title,
    labeled_text_area,
    labeled_number_input,
    labeled_selectbox,
    labeled_multiselect,
)
from core_functions import (
    suggest_max_experience,
    suggest_language_levels,
    suggest_certifications,
    get_index_for_value,
)
from error_handling import handle_error
from data_processing import validate_text_length

def main():
    """Functions of the skills page of the Streamlit application."""
    centered_title("Skills")

    # Initialize Session State if not existing
    if "job_details" not in st.session_state:
        st.session_state.job_details = {}

    # Required Skills
    st.session_state.job_details["required_skills"] = labeled_text_area(
        "Required Skills",
        "required_skills",
        value=st.session_state.job_details.get("required_skills", ""),
        placeholder="Enter the required skills (e.g. Python, Java, SQL)",
        height=100,
        help_text="Enter the skills that are essential for the position.",
    )

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.job_details["experience_level_min_req"] = labeled_number_input(
            "Min. Experience (Years)",
            "experience_level_min_req",
            value=st.session_state.job_details.get("experience_level_min_req", 0),
            min_value=0,
            help_text="Minimum professional experience in years",
        )
    with col2:
        st.session_state.job_details["experience_level_max_req"] = labeled_number_input(
            "Max. Experience (Years)",
            "experience_level_max_req",
            value=st.session_state.job_details.get("experience_level_max_req", 0),
            min_value=0,
            help_text="Maximum professional experience in years",
        )

    # Experience level correlation
    if st.session_state.job_details["experience_level_min_req"]:
        suggested_max_experience = suggest_max_experience(
            st.session_state.job_details["experience_level_min_req"]
        )
        if suggested_max_experience:
            if st.button(
                f"Is a maximum experience level of {suggested_max_experience} years appropriate?"
            ):
                st.session_state.job_details["experience_level_max_req"] = (
                    suggested_max_experience
                )
                st.rerun()

    # Technical Skills
    st.session_state.job_details["technical_skills"] = labeled_text_area(
        "Technical Skills",
        "technical_skills",
        value=st.session_state.job_details.get("technical_skills", ""),
        placeholder="Enter the technical skills (e.g. AWS, Azure, GCP)",
        height=100,
        help_text="Enter the technical skills that are relevant for the position.",
    )

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.job_details["experience_level_min_tech"] = labeled_number_input(
            "Min. Experience (Years)",
            "experience_level_min_tech",
            value=st.session_state.job_details.get("experience_level_min_tech", 0),
            min_value=0,
            help_text="Minimum professional experience in years",
        )
    with col2:
        st.session_state.job_details["experience_level_max_tech"] = labeled_number_input(
            "Max. Experience (Years)",
            "experience_level_max_tech",
            value=st.session_state.job_details.get("experience_level_max_tech", 0),
            min_value=0,
            help_text="Maximum professional experience in years",
        )

    # Soft Skills
    st.session_state.job_details["soft_skills"] = labeled_text_area(
        "Soft Skills",
        "soft_skills",
        value=st.session_state.job_details.get("soft_skills", ""),
        placeholder="Enter the soft skills (e.g. communication, teamwork)",
        height=100,
        help_text="Enter the soft skills that are relevant for the position.",
    )

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.job_details["experience_level_min_soft"] = labeled_number_input(
            "Min. Experience (Years)",
            "experience_level_min_soft",
            value=st.session_state.job_details.get("experience_level_min_soft", 0),
            min_value=0,
            help_text="Minimum professional experience in years",
        )
    with col2:
        st.session_state.job_details["experience_level_max_soft"] = labeled_number_input(
            "Max. Experience (Years)",
            "experience_level_max_soft",
            value=st.session_state.job_details.get("experience_level_max_soft", 0),
            min_value=0,
            help_text="Maximum professional experience in years",
        )

    # Languages
    st.session_state.job_details["required_languages"] = labeled_text_area(
        "Required Languages",
        "required_languages",
        value=st.session_state.job_details.get("required_languages", ""),
        placeholder="Enter the required languages (e.g. German, English, Spanish)",
        height=100,
        help_text="Enter the languages that are required for the position.",
    )

    # Language level suggestions
    if st.session_state.job_details["required_languages"]:
        language_levels = suggest_language_levels(
            st.session_state.job_details["required_languages"]
        )
        if language_levels:
            for language, level in language_levels.items():
                st.session_state.job_details[f"{language}_level"] = labeled_selectbox(
                    f"Language proficiency for {language}",
                    ["A1", "A2", "B1", "B2", "C1", "C2"],
                    f"level_{language}",
                    index=get_index_for_value(
                        level, ["A1", "A2", "B1", "B2", "C1", "C2"]
                    ),
                    help_text=f"Select the language proficiency level for {language}.",
                )

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.job_details["experience_level_min_lang"] = labeled_number_input(
            "Min. Experience (Years)",
            "experience_level_min_lang",
            value=st.session_state.job_details.get("experience_level_min_lang", 0),
            min_value=0,
            help_text="Minimum professional experience in years",
        )
    with col2:
        st.session_state.job_details["experience_level_max_lang"] = labeled_number_input(
            "Max. Experience (Years)",
            "experience_level_max_lang",
            value=st.session_state.job_details.get("experience_level_max_lang", 0),
            min_value=0,
            help_text="Maximum professional experience in years",
        )

    # Education
    st.session_state.job_details["education_level"] = labeled_text_input(
        "Education Level",
        "education_level",
        value=st.session_state.job_details.get("education_level", ""),
        placeholder="e.g. Bachelor, Master, PhD",
        help_text="Enter the desired educational qualification.",
    )

    # Certifications
    st.session_state.job_details["desired_certifications"] = labeled_text_area(
        "Desired Certifications",
        "desired_certifications",
        value=st.session_state.job_details.get("desired_certifications", ""),
        placeholder="e.g. AWS Certified Solutions Architect, PMP",
        height=100,
        help_text="Enter desired certifications for the position.",
    )

    # Certification suggestions
    if st.session_state.job_details["technical_skills"]:
        suggested_certifications = suggest_certifications(
            st.session_state.job_details["technical_skills"]
        )
        if suggested_certifications:
            st.session_state.job_details["desired_certifications"] = labeled_multiselect(
                "Relevant Certifications",
                suggested_certifications,
                "selected_certifications",
                default=st.session_state.job_details["desired_certifications"]
                if "desired_certifications" in st.session_state.job_details
                else [],
                help_text="Select relevant certifications from the list.",
            )

    if st.button("Next: Benefits"):
        # Validation of text length for Required Skills
        if not validate_text_length(
            st.session_state.job_details.get("required_skills", ""), 500
        ):
            st.error(
                "The 'Required Skills' field must be a maximum of 500 characters long."
            )
            return

        # Validation of text length for Technical Skills
        if not validate_text_length(
            st.session_state.job_details.get("technical_skills", ""), 500
        ):
            st.error(
                "The 'Technical Skills' field must be a maximum of 500 characters long."
            )
            return

        # Validation of text length for Soft Skills
        if not validate_text_length(
            st.session_state.job_details.get("soft_skills", ""), 500
        ):
            st.error("The 'Soft Skills' field must be a maximum of 500 characters long.")
            return

        # Validation of text length for Required Languages
        if not validate_text_length(
            st.session_state.job_details.get("required_languages", ""), 500
        ):
            st.error(
                "The 'Required Languages' field must be a maximum of 500 characters long."
            )
            return

        # Validation of text length for Education Level
        if not validate_text_length(
            st.session_state.job_details.get("education_level", ""), 300
        ):
            st.error(
                "The 'Education Level' field must be a maximum of 300 characters long."
            )
            return

        # Validation of text length for Desired Certifications
        if not validate_text_length(
            st.session_state.job_details.get("desired_certifications", ""), 500
        ):
            st.error(
                "The 'Desired Certifications' field must be a maximum of 500 characters long."
            )
            return

        st.session_state.current_page = "benefits_page"
        st.rerun()

if __name__ == "__main__":
    main()