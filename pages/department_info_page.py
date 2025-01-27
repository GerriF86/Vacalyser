# pages/3_department_info_page.py
import streamlit as st
from core_functions import get_index_for_value, get_department_keywords, estimate_team_size
from ui_elements import (
    centered_title,
    labeled_selectbox,
    labeled_text_input,
    labeled_number_input,
    labeled_multiselect
)
from data_processing import validate_email_address, validate_phone_number, validate_text_length

def main():
    """Functions of the department information page of the Streamlit application."""
    centered_title("Department Information")

    # Initialize Session State if not existing
    if "job_details" not in st.session_state:
        st.session_state.job_details = {}

    # Input fields with extended logic and validation
    departments = [
        "IT",
        "Marketing",
        "Sales",
        "HR",
        "Finance",
        "R&D",
        "Production",
        "Customer Service",
        "Legal",
        "Logistics",
    ]
    st.session_state.job_details["department"] = labeled_selectbox(
        "Department",
        departments,
        "department",
        index=get_index_for_value(
            st.session_state.job_details.get("department"), departments
        ),
        help_text="Select the department for which the position is being advertised."
    )

    # Dependent keyword suggestions
    if st.session_state.job_details["department"]:
        suggested_keywords = get_department_keywords(
            st.session_state.job_details["department"]
        )
        st.session_state.job_details["department_keywords"] = labeled_multiselect(
            "Keywords for the Department (e.g. Cloud, DevOps, Security)",
            suggested_keywords,
            "department_keywords",
            default=st.session_state.job_details.get("department_keywords", []),
            help_text="Select keywords that best describe the department."
        )

    st.session_state.company_info["department_size"] = labeled_number_input(
        "Department Size",
        "department_size",
        value=st.session_state.company_info.get("department_size", 1),
        min_value=1,
        help_text="Enter the approximate number of employees in the department."
    )

    # Team size estimation with validation
    if st.session_state.company_info["department_size"]:
        estimated_team_size = estimate_team_size(
            st.session_state.company_info["department_size"]
        )

        team_size_input = labeled_number_input(
            f"Team Size (estimated: {estimated_team_size})",
            "team_size",
            value=st.session_state.job_details.get("team_size", estimated_team_size),
            min_value=1,
            help_text="Enter the approximate size of the team to which the new position belongs."
        )

        if st.button(
            f"Is the team size typical (approx. {estimated_team_size} employees)?"
        ):
            if team_size_input <= st.session_state.company_info["department_size"]:
                st.session_state.job_details["team_size"] = estimated_team_size
            else:
                st.error(
                    "The team size cannot be larger than the department size."
                )

        if team_size_input <= st.session_state.company_info["department_size"]:
            st.session_state.job_details["team_size"] = team_size_input
        else:
            st.error(
                "The team size cannot be larger than the department size."
            )

    st.session_state.job_details["reporting_line"] = labeled_text_input(
        "Reporting Line",
        "reporting_line",
        value=st.session_state.job_details.get("reporting_line", ""),
        placeholder="e.g. Head of Marketing",
        help_text="Enter the position or person to whom the new position reports."
    )

    st.session_state.job_details["internal_contact"] = labeled_text_input(
        "Internal Contact Person",
        "internal_contact",
        value=st.session_state.job_details.get("internal_contact", ""),
        placeholder="e.g. Max Mustermann",
        help_text="Enter the name of the internal contact person for this position."
    )

    # Budget Authority assignment with validation
    if (
        st.session_state.job_details["reporting_line"]
        and st.session_state.job_details["direct_supervisor"]
    ):
        budget_authority_options = [
            st.session_state.job_details["direct_supervisor"],
            st.session_state.job_details["reporting_line"],
            "Other",
        ]
        st.session_state.job_details["budget_authority"] = labeled_selectbox(
            "Who has the budget responsibility?",
            budget_authority_options,
            "budget_authority",
            index=get_index_for_value(
                st.session_state.job_details.get("budget_authority"),
                budget_authority_options,
            ),
            help_text="Select the person who has the budget responsibility for this position."
        )
        if st.session_state.job_details["budget_authority"] == "Other":
            st.session_state.job_details["budget_authority"] = labeled_text_input(
                "Please enter name or position",
                "budget_authority_other",
                value="",
                help_text="Enter the name or position of the person responsible for the budget."
            )

    st.session_state.job_details["hiring_authority"] = labeled_text_input(
        "Hiring Authority",
        "hiring_authority",
        value=st.session_state.job_details.get("hiring_authority", ""),
        placeholder="e.g. Department Head",
        help_text="Enter the position or person who has the hiring authority for this position."
    )

    st.session_state.job_details["requisition_originator"] = labeled_text_input(
        "Requester",
        "requisition_originator",
        value=st.session_state.job_details.get("requisition_originator", ""),
        placeholder="e.g. HR Manager",
        help_text="Enter the position or person who requested the job posting."
    )

    st.session_state.job_details["direct_supervisor"] = labeled_text_input(
        "Direct Supervisor",
        "direct_supervisor",
        value=st.session_state.job_details.get("direct_supervisor", ""),
        placeholder="e.g. Team Leader",
        help_text="Enter the position or person who will be the direct supervisor of the new position."
    )

    st.session_state.job_details["contact_email_hiring"] = labeled_text_input(
        "Email (Hiring Authority)",
        "contact_email_hiring",
        value=st.session_state.job_details.get("contact_email_hiring", ""),
        placeholder="e.g. max.mustermann@example.com",
        help_text="Enter the email address of the person with hiring authority."
    )
    if st.session_state.job_details["contact_email_hiring"]:
        if not validate_email_address(
            st.session_state.job_details["contact_email_hiring"]
        ):
            st.error("Please enter a valid email address.")

    st.session_state.job_details["contact_phone_hiring"] = labeled_text_input(
        "Phone (Hiring Authority)",
        "contact_phone_hiring",
        value=st.session_state.job_details.get("contact_phone_hiring", ""),
        placeholder="e.g. +49 123 456789",
        help_text="Enter the phone number of the person with hiring authority."
    )
    if st.session_state.job_details["contact_phone_hiring"]:
        if not validate_phone_number(
            st.session_state.job_details["contact_phone_hiring"]
        ):
            st.error("Please enter a valid phone number.")

    st.session_state.job_details["contact_email_requisition"] = labeled_text_input(
        "Email (Requester)",
        "contact_email_requisition",
        value=st.session_state.job_details.get("contact_email_requisition", ""),
        placeholder="e.g. maria.musterfrau@example.com",
        help_text="Enter the email address of the requester."
    )
    if st.session_state.job_details["contact_email_requisition"]:
        if not validate_email_address(
            st.session_state.job_details["contact_email_requisition"]
        ):
            st.error("Please enter a valid email address.")

    st.session_state.job_details["contact_phone_requisition"] = labeled_text_input(
        "Phone (Requester)",
        "contact_phone_requisition",
        value=st.session_state.job_details.get("contact_phone_requisition", ""),
        placeholder="e.g. +49 987 654321",
        help_text="Enter the phone number of the requester."
    )
    if st.session_state.job_details["contact_phone_requisition"]:
        if not validate_phone_number(
            st.session_state.job_details["contact_phone_requisition"]
        ):
            st.error("Please enter a valid phone number.")

    if st.button("Next: Role Info"):
        # Validation of required fields
        required_fields = ["department", "department_size", "team_size"]
        for field in required_fields:
            if not st.session_state.job_details.get(field):
                st.error(
                    f"Please fill in the field '{field.replace('_', ' ').capitalize()}'."
                )
                return  # Stop execution if a required field is missing

            if field in st.session_state.job_details and not validate_text_length(st.session_state.job_details[field], 100):
                st.error(
                    f"The field '{field.replace('_', ' ').capitalize()}' must be a maximum of 100 characters long."
                )
                return

        st.session_state.current_page = "role_info"
        st.rerun()

if __name__ == "__main__":
    main()