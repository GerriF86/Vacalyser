import streamlit as st
from utils import styled_button

def main():
    job_title = st.session_state.job_details["job_title"]
    st.header(f"Benefits for {job_title}")

    st.session_state.company_info["competitor_companies"] = st.text_area(
        "Competitor Companies",
        value=st.session_state.company_info.get("competitor_companies", "")
    )
    st.session_state.job_details["tools_technologies"] = st.text_area(
        "Tools and Technologies",
        value=st.session_state.job_details.get("tools_technologies", "")
    )

    if "selected_benefits" not in st.session_state:
        st.session_state.selected_benefits = []

    st.subheader("Classic Benefits")
    for benefit, benefit_type in st.session_state.benefits.items():
        if benefit_type["classic"]:
            if st.checkbox(benefit, key=benefit):
                if benefit not in st.session_state.selected_benefits:
                    st.session_state.selected_benefits.append(benefit)
            else:
                if benefit in st.session_state.selected_benefits:
                    st.session_state.selected_benefits.remove(benefit)

    st.subheader("Innovative Benefits")
    for benefit, benefit_type in st.session_state.benefits.items():
        if benefit_type["innovative"]:
            if st.checkbox(benefit, key=benefit):
                if benefit not in st.session_state.selected_benefits:
                    st.session_state.selected_benefits.append(benefit)
            else:
                if benefit in st.session_state.selected_benefits:
                    st.session_state.selected_benefits.remove(benefit)

    # Button Layout anpassen
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("Next: Summary"):
            st.session_state.page = "summary_page"
            st.rerun()