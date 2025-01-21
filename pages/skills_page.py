import streamlit as st
from utils import styled_button

def main():
    # Seitentitel
    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            <div style='color: #696969; font-size: 2em; font-weight: 700; line-height: 1.2; text-align: left;'>Skills</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.session_state.job_details["required_skills"] = st.text_area("Required Skills", value=", ".join(st.session_state.job_details.get("required_skills", [])))
        st.session_state.job_details["experience_level_min_req"] = st.number_input("Minimum Experience Level (Required)", value=st.session_state.job_details.get("experience_level_min_req", 0), min_value=0)
        st.session_state.job_details["experience_level_max_req"] = st.number_input("Maximum Experience Level (Required)", value=st.session_state.job_details.get("experience_level_max_req", 0), min_value=0)
        st.session_state.job_details["technical_skills"] = st.text_area("Technical Skills", value=", ".join(st.session_state.job_details.get("technical_skills", [])))
        st.session_state.job_details["experience_level_min_tech"] = st.number_input("Minimum Experience Level (Technical)", value=st.session_state.job_details.get("experience_level_min_tech", 0), min_value=0)
        st.session_state.job_details["experience_level_max_tech"] = st.number_input("Maximum Experience Level (Technical)", value=st.session_state.job_details.get("experience_level_max_tech", 0), min_value=0)
        st.session_state.job_details["desired_certifications"] = st.text_area("Desired Certifications", value=", ".join(st.session_state.job_details.get("desired_certifications", [])))
        st.session_state.job_details["education_level"] = st.text_input("Education Level", value=st.session_state.job_details.get("education_level", ""))

    with col2:
        st.session_state.job_details["soft_skills"] = st.text_area("Soft Skills", value=", ".join(st.session_state.job_details.get("soft_skills", [])))
        st.session_state.job_details["experience_level_min_soft"] = st.number_input("Minimum Experience Level (Soft)", value=st.session_state.job_details.get("experience_level_min_soft", 0), min_value=0)
        st.session_state.job_details["experience_level_max_soft"] = st.number_input("Maximum Experience Level (Soft)", value=st.session_state.job_details.get("experience_level_max_soft", 0), min_value=0)
        st.session_state.job_details["required_languages"] = st.text_area("Required Languages", value=", ".join(st.session_state.job_details.get("required_languages", [])))
        st.session_state.job_details["experience_level_min_lang"] = st.number_input("Minimum Experience Level (Languages)", value=st.session_state.job_details.get("experience_level_min_lang", 0), min_value=0)
        st.session_state.job_details["experience_level_max_lang"] = st.number_input("Maximum Experience Level (Languages)", value=st.session_state.job_details.get("experience_level_max_lang", 0), min_value=0)

    # Button Layout anpassen
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("Next: Tasks"):
            st.session_state.page = "tasks_page"
            st.rerun()