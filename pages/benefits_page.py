# pages/6_benefits_page.py
import streamlit as st
from ui_elements import (
    centered_title,
    labeled_checkbox,
    section_title,
)
from core_functions import (
    get_competitor_benefits,
    get_job_specific_benefits,
    get_regional_benefits,
    estimate_benefit_costs
)
from error_handling import handle_error

def main():
    """Functions of the benefits page of the Streamlit application."""
    centered_title("Benefits")

    # Initialize Session State if not existing
    if "company_info" not in st.session_state:
        st.session_state.company_info = {}
    if "job_details" not in st.session_state:
        st.session_state.job_details = {}
    if "selected_benefits" not in st.session_state:
        st.session_state.selected_benefits = []

    # Predefined benefits (can be extended)
    classic_benefits = [
        "Company Pension Scheme",
        "Health Insurance",
        "Flexible Working Hours",
        "Home Office Options",
        "Training Opportunities",
        "Company Car",
        "Meal Allowance",
        "Employee Discounts",
        "Sports and Fitness Offers",
        "Company Kindergarten",
        "Paid Parental Leave",
        "Public Transport Ticket",
    ]
    innovative_benefits = [
        "Sabbatical Options",
        "Workation Opportunities",
        "Mental Health Support",
        "Pet-friendly Workplace",
        "Volunteer Days",
        "Stock Options",
        "Profit Sharing",
        "Environmentally Friendly Mobility Solutions (e.g. Job Bike)",
        "Lifelong Learning Budget",
        "Free Snacks and Drinks",
        "On-site Gym",
        "Wellness Programs",
    ]

    # Competitor benchmarking
    if "competitor_companies" in st.session_state.company_info:
        try:
            competitor_benefits = get_competitor_benefits(
                st.session_state.company_info["competitor_companies"]
            )
            if competitor_benefits:
                section_title("Benefits of Competitor Companies")
                for company, benefits in competitor_benefits.items():
                    st.write(f"**{company}**")
                    for benefit in benefits:
                        st.write(f"- {benefit}")
                    if st.button(
                        f"Copy Benefits from {company}",
                        key=f"copy_benefits_{company}",
                    ):
                        for benefit in benefits:
                            if benefit not in st.session_state.selected_benefits:
                                st.session_state.selected_benefits.append(benefit)
                        st.rerun()
        except Exception as e:
            handle_error(e, "Error retrieving competitor benefits.")

    # Position-specific benefits
    if "job_title" in st.session_state.job_details:
        try:
            job_specific_benefits = get_job_specific_benefits(
                st.session_state.job_details["job_title"]
            )
            if job_specific_benefits:
                section_title("Common Benefits for this Position")
                for benefit in job_specific_benefits:
                    st.write(f"- {benefit}")
                    if st.button(f"Add {benefit}", key=f"add_benefit_{benefit}"):
                        if benefit not in st.session_state.selected_benefits:
                            st.session_state.selected_benefits.append(benefit)
                            st.rerun()
        except Exception as e:
            handle_error(e, "Error retrieving position-specific benefits.")

    # Regional differences
    if "job_location" in st.session_state.job_details:
        try:
            regional_benefits = get_regional_benefits(
                st.session_state.job_details["job_location"]
            )
            if regional_benefits:
                section_title("Common Benefits in this Region")
                for benefit in regional_benefits:
                    st.write(f"- {benefit}")
                    if st.button(
                        f"Add {benefit}", key=f"add_regional_benefit_{benefit}"
                    ):
                        if benefit not in st.session_state.selected_benefits:
                            st.session_state.selected_benefits.append(benefit)
                            st.rerun()
        except Exception as e:
            handle_error(e, "Error retrieving regional benefits.")

    # Trend analysis (Example - would need to be expanded with current market data)
    section_title("Current Trends")
    current_trends = [
        "Work-Life Balance",
        "Sustainability",
        "Employee Development",
        "Remote Work",
        "Health and Wellness",
    ]
    for trend in current_trends:
        st.write(f"- {trend}")

    # Selection of benefits with checkboxes in two columns
    col1, col2 = st.columns(2)
    with col1:
        section_title("Classic Benefits")
        for benefit in classic_benefits:
            is_selected = labeled_checkbox(
                benefit,
                benefit,
                value=benefit in st.session_state.selected_benefits,
                help_text="Select this benefit if it is offered by the company.",
            )
            if is_selected:
                if benefit not in st.session_state.selected_benefits:
                    st.session_state.selected_benefits.append(benefit)
            else:
                if benefit in st.session_state.selected_benefits:
                    st.session_state.selected_benefits.remove(benefit)

    with col2:
        section_title("Innovative Benefits")
        for benefit in innovative_benefits:
            is_selected = labeled_checkbox(
                benefit,
                benefit,
                value=benefit in st.session_state.selected_benefits,
                help_text="Select this benefit if it is offered by the company.",
            )
            if is_selected:
                if benefit not in st.session_state.selected_benefits:
                    st.session_state.selected_benefits.append(benefit)
            else:
                if benefit in st.session_state.selected_benefits:
                    st.session_state.selected_benefits.remove(benefit)

    # Cost-benefit analysis (Example - would need to be expanded with realistic data)
    if st.session_state.selected_benefits:
        try:
            estimated_cost = estimate_benefit_costs(st.session_state.selected_benefits)
            st.write(
                f"Estimated cost of the selected benefits: {estimated_cost} per year and employee"
            )
        except Exception as e:
            handle_error(e, "Error in cost-benefit analysis.")

    if st.button("Next: Recruitment Process"):
        st.session_state.current_page = "recruitment_process_page"
        st.rerun()

if __name__ == "__main__":
    main()