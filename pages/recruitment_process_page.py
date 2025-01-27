# pages/7_recruitment_process_page.py
import streamlit as st
from ui_elements import centered_title, labeled_text_area, labeled_number_input, labeled_text_input
from data_processing import validate_text_length

def main():
    """Functions of the recruitment process page of the Streamlit application."""
    centered_title("Recruitment Process")

    # Initialize Session State if not existing
    if "job_details" not in st.session_state:
        st.session_state.job_details = {}
    if "recruitment_process_steps" not in st.session_state:
        st.session_state.recruitment_process_steps = [
            "CV Screening",
            "Phone Interview",
            "Technical Interview",
            "Team Interview",
            "HR Interview",
            "Assessment Center",
            "Final Interview",
            "Contract Negotiation",
        ]
    if "selected_recruitment_steps" not in st.session_state:
        st.session_state.selected_recruitment_steps = []

    # Selection of recruitment process steps with checkboxes in two columns
    col1, col2 = st.columns(2)
    for i, step in enumerate(st.session_state.recruitment_process_steps):
        with col1 if i % 2 == 0 else col2:
            is_selected = st.checkbox(
                step,
                key=f"recruitment_step_{step}",
                value=step in st.session_state.selected_recruitment_steps,
            )
            if is_selected:
                if step not in st.session_state.selected_recruitment_steps:
                    st.session_state.selected_recruitment_steps.append(step)
            else:
                if step in st.session_state.selected_recruitment_steps:
                    st.session_state.selected_recruitment_steps.remove(step)

    # Additional details for each selected step
    for step in st.session_state.selected_recruitment_steps:
        st.write(f"**{step}**")
        st.session_state.job_details[f"duration_{step}"] = labeled_number_input(
            f"Duration of '{step}' (in days)",
            f"duration_{step}",
            value=st.session_state.job_details.get(f"duration_{step}", 0),
            min_value=0,
            help_text="Enter the estimated duration of this step in days.",
        )
        st.session_state.job_details[f"responsible_{step}"] = labeled_text_input(
            f"Responsible for '{step}'",
            f"responsible_{step}",
            value=st.session_state.job_details.get(f"responsible_{step}", ""),
            placeholder="e.g. HR, Team Lead",
            help_text="Enter the person or department responsible for this step.",
        )

    # Current recruitment process
    st.session_state.job_details["current_recruitment_process"] = labeled_text_area(
        "Current Recruitment Process",
        "current_recruitment_process",
        value=st.session_state.job_details.get("current_recruitment_process", ""),
        placeholder="Describe the current recruitment process.",
        height=150,
        help_text="Enter a description of the current recruitment process."
    )

    if st.button("Next: Summary"):
        # Validation of text length for Recruitment Process Description
        if not validate_text_length(
            st.session_state.job_details.get("current_recruitment_process", ""), 500
        ):
            st.error(
                "The 'Current Recruitment Process' description must be a maximum of 500 characters long."
            )
            return

        st.session_state.current_page = "summary_page"
        st.rerun()

if __name__ == "__main__":
    main()