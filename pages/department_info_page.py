import streamlit as st
from utils import styled_button

def main():
    # Seitentitel
    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            <div style='color: #696969; font-size: 2em; font-weight: 700; line-height: 1.2; text-align: left;'>Department Info</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        # Department Dropdown
        department_options = ["Admin", "HR", "IT", "Sales", "Marketing", "Finance", "Engineering", "Other"]
        st.session_state.job_details["department"] = st.selectbox("Department", department_options, index=department_options.index(st.session_state.job_details["department"]) if st.session_state.job_details["department"] in department_options else 0)

        st.session_state.job_details["department_keywords"] = st.text_area(
            "Department-specific Keywords",
            value=st.session_state.job_details["department_keywords"],placeholder="e.g., agile, Scrum, data analysis",
        )
        st.session_state.company_info["department_size"] = st.number_input("Department Size", value=st.session_state.company_info.get("department_size", 0), min_value=0)
        st.session_state.job_details["team_size"] = st.number_input("Team Size", value=st.session_state.job_details.get("team_size", 0), min_value=0)
        st.session_state.company_info["company_culture"] = st.text_area("Company Culture", value=st.session_state.company_info.get("company_culture", ""))
        st.session_state.job_details["reporting_line"] = st.text_input("Reporting Line", value=st.session_state.job_details.get("reporting_line", ""))

    with col2:
        st.session_state.job_details["internal_contact"] = st.text_input("Internal Contact", value=st.session_state.job_details.get("internal_contact", ""))
        st.session_state.job_details["budget_authority"] = st.text_input("Budget Authority", value=st.session_state.job_details.get("budget_authority", ""))
        st.session_state.job_details["contact_email"] = st.text_input("Contact Email", value=st.session_state.job_details.get("contact_email", ""))
        st.session_state.job_details["hiring_authority"] = st.text_input("Hiring Authority", value=st.session_state.job_details.get("hiring_authority", ""))
        st.session_state.job_details["requisition_originator"] = st.text_input("Requisition Originator", value=st.session_state.job_details.get("requisition_originator", ""))
        st.session_state.job_details["direct_supervisor"] = st.text_input("Direct Supervisor", value=st.session_state.job_details.get("direct_supervisor", ""))

    # Button Layout anpassen
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("Next: Job Details"):
            st.session_state.page = "job_details_page"
            st.rerun()