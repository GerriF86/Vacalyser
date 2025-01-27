# pages/4_role_info_page.py
import streamlit as st
from core_functions import estimate_salary_range, get_index_for_value, get_contract_type_suggestions
from ui_elements import (
    centered_title,
    labeled_text_input,
    labeled_selectbox,
    labeled_date_input,
    labeled_number_input,
)
from data_processing import validate_salary_range, validate_text_length
from error_handling import handle_error

def main():
    """Functions of the role information page of the Streamlit application."""
    centered_title("Role Information")

    # Initialize Session State if not existing
    if "job_details" not in st.session_state:
        st.session_state.job_details = {}

    # Input fields with logic and suggestions
    st.session_state.job_details["job_title"] = labeled_text_input(
        "Job Title",
        "job_title",
        value=st.session_state.job_details.get("job_title", ""),
        help_text="Enter the job title of the position (e.g. Data Scientist, Software Engineer).",
    )

    # Contract type suggestions
    if (
        st.session_state.job_details["job_title"]
        and st.session_state.company_info.get("industry")
    ):
        suggested_contract_types = get_contract_type_suggestions(
            st.session_state.job_details["job_title"],
            st.session_state.company_info["industry"],
        )
        st.session_state.job_details["contract_type"] = labeled_selectbox(
            "Contract Type",
            suggested_contract_types,
            "contract_type",
            index=get_index_for_value(
                st.session_state.job_details.get("contract_type"),
                suggested_contract_types,
            ),
            help_text="Select the type of employment contract."
        )

    st.session_state.job_details["start_date"] = labeled_date_input(
        "Start Date",
        "start_date",
        value=st.session_state.job_details.get("start_date"),
        help_text="Select the desired start date."
    )

    st.session_state.job_details["job_location"] = labeled_text_input(
        "Work Location",
        "job_location",
        value=st.session_state.job_details.get("job_location", ""),
        help_text="Enter the location where the work will be performed."
    )

    st.session_state.job_details["onsite_percentage"] = labeled_number_input(
        "Onsite Percentage (%)",
        "onsite_percentage",
        value=st.session_state.job_details.get("onsite_percentage", 0),
        min_value=0,
        max_value=100,
        help_text="Enter the percentage of work to be performed on-site."
    )

    # Work model restriction
    if st.session_state.job_details["job_location"]:
        suggested_work_model = get_work_model_suggestion(
            st.session_state.job_details["job_location"]
        )
        work_model_options = ["Onsite", "Remote", "Hybrid"]
        st.session_state.job_details["work_model"] = labeled_selectbox(
            "Work Model",
            work_model_options,
            "work_model",
            index=get_index_for_value(
                st.session_state.job_details.get("work_model"), work_model_options
            ),
            help_text="Select the applicable work model (onsite, remote, hybrid)."
        )
        if suggested_work_model:
            st.write(
                f"For this location, the following work model is conceivable: {suggested_work_model}."
            )

    st.session_state.job_details["work_arrangement"] = labeled_text_input(
        "Work Arrangements",
        "work_arrangement",
        value=st.session_state.job_details.get("work_arrangement", ""),
        placeholder="e.g. flextime, trust-based working hours",
        help_text="Enter special work arrangements or conditions."
    )

    st.session_state.job_details["travel_requirements"] = labeled_text_input(
        "Travel Requirements",
        "travel_requirements",
        value=st.session_state.job_details.get("travel_requirements", ""),
        placeholder="e.g. occasional business trips",
        help_text="Indicate what travel is associated with the position."
    )

    # Travel percentage estimation
    if st.session_state.job_details["travel_requirements"]:
        estimated_travel_percentage = estimate_travel_percentage(
            st.session_state.job_details["travel_requirements"]
        )
        if estimated_travel_percentage:
            st.session_state.job_details["travel_percentage"] = labeled_number_input(
                f"Estimated Proportion of Travel ({estimated_travel_percentage}%)",
                "travel_percentage",
                value=estimated_travel_percentage,
                min_value=0,
                max_value=100,
                help_text="Enter the estimated percentage of travel."
            )

    st.session_state.job_details["priority"] = labeled_selectbox(
        "Priority",
        ["High", "Medium", "Low"],
        "priority",
        index=get_index_for_value(
            st.session_state.job_details.get("priority"), ["High", "Medium", "Low"]
        ),
        help_text="Select the priority for filling this position."
    )

    st.session_state.job_details["training_budget"] = labeled_number_input(
        "Training Budget",
        "training_budget",
        value=st.session_state.job_details.get("training_budget", 0),
        help_text="Enter the available training budget for this position."
    )

    st.session_state.job_details["salary_range"] = labeled_text_input(
        "Salary Range (e.g. 60k-80k)",
        "salary_range",
        value=st.session_state.job_details.get("salary_range", ""),
        help_text="Enter the salary range for this position (e.g. 60k-80k)."
    )

    # Salary range refinement with validation
    if st.session_state.job_details["salary_range"]:
        if validate_salary_range(st.session_state.job_details["salary_range"]):
            salary_range_warning = check_salary_range(
                st.session_state.job_details["salary_range"]
            )
            if salary_range_warning:
                st.warning(salary_range_warning)
        else:
            st.error(
                "Invalid format for salary range. Please use the format 'lower limit k-upper limit k'."
            )

    st.session_state.job_details["vacancy_reason"] = labeled_text_input(
        "Reason for Vacancy",
        "vacancy_reason",
        value=st.session_state.job_details.get("vacancy_reason", ""),
        placeholder="e.g. parental leave replacement, newly created position",
        help_text="Enter the reason why this position is vacant."
    )

    # Estimation of salary range
    with st.expander("Salary Proposal (estimated)"):
        experience_levels = ["Junior", "Mid-Level", "Senior", "Lead", "Principal"]
        st.session_state.job_details["experience_level"] = labeled_selectbox(
            "Experience Level",
            experience_levels,
            "experience_level",
            index=get_index_for_value(
                st.session_state.job_details.get("experience_level"), experience_levels
            ),
            help_text="Select the expected experience level for this position."
        )
        if st.button("Estimate Salary Range"):
            if (
                st.session_state.job_details["job_title"]
                and st.session_state.job_details["experience_level"]
            ):
                try:
                    estimated_salary = estimate_salary_range(
                        st.session_state.job_details["job_title"],
                        st.session_state.job_details["experience_level"],
                    )
                    st.write(f"Estimated Salary Range: {estimated_salary}")
                except Exception as e:
                    handle_error(e, "Error in salary estimation.")
            else:
                st.write("Please enter job title and experience level.")

    if st.button("Next: Skills"):
        # Validation of required fields
        required_fields = ["job_title", "start_date", "job_location"]
        for field in required_fields:
            if not st.session_state.job_details.get(field):
                st.error(
                    f"Please fill in the field '{field.replace('_', ' ').capitalize()}'."
                )
                return  # Stop execution if a required field is missing

        # Validation of text length for other relevant fields
        text_fields_to_validate = [
            "work_arrangement",
            "travel_requirements",
            "vacancy_reason",
        ]
        for field in text_fields_to_validate:
            if (
                field in st.session_state.job_details
                and not validate_text_length(
                    st.session_state.job_details[field], 300
                )
            ):
                st.error(
                    f"The field '{field.replace('_', ' ').capitalize()}' must be a maximum of 300 characters long."
                )
                return

        st.session_state.current_page = "tasks_page"
        st.rerun()

if __name__ == "__main__":
    main()