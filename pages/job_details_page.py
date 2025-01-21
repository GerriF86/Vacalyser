import streamlit as st
from utils import styled_button

def main():
    # Seitentitel
    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            <div style='color: #696969; font-size: 2em; font-weight: 700; line-height: 1.2; text-align: left;'>job_details</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.session_state.job_details["job_title"] = st.text_input("Job Title", value=st.session_state.job_details.get("job_title", ""))
        st.session_state.job_details["start_date"] = st.date_input("Start Date", value=st.session_state.job_details.get("start_date", None))
        st.session_state.job_details["contract_type"] = st.text_input("Contract Type", value=st.session_state.job_details.get("contract_type", ""))
        st.session_state.job_details["job_location"] = st.text_input("Job Location", value=st.session_state.job_details.get("job_location", ""))
        st.session_state.job_details["onsite_percentage"] = st.number_input("Onsite Percentage", min_value=0, max_value=100, value=st.session_state.job_details.get("onsite_percentage", 0), format="%d%%")
        st.session_state.job_details["work_arrangement"] = st.text_input("Work Arrangement", value=st.session_state.job_details.get("work_arrangement", ""))
        st.session_state.job_details["work_model"] = st.text_input("Work Model", value=st.session_state.job_details.get("work_model", ""))
        st.session_state.job_details["travel_requirements"] = st.text_input("Travel Requirements", value=st.session_state.job_details.get("travel_requirements", ""))

    with col2:
        # Dropdown für die Priorität
        priority_options = ["High", "Medium", "Low"]
        current_priority = st.session_state.job_details.get("priority", "Low")
        current_priority_index = priority_options.index(current_priority) if current_priority in priority_options else 0
        st.session_state.job_details["priority"] = st.selectbox("Priority", priority_options, index=current_priority_index)

        st.session_state.job_details["training_budget"] = st.number_input("Training Budget", value=st.session_state.job_details.get("training_budget", 0))
        st.session_state.job_details["salary_range"] = st.text_input("Salary Range", value=st.session_state.job_details.get("salary_range", ""))
        st.session_state.job_details["vacancy_reason"] = st.text_input("Reason for Vacancy", value=st.session_state.job_details.get("vacancy_reason", ""))

    # Button Layout anpassen
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("Next: Skills"):
            st.session_state.page = "skills_page"
            st.rerun()