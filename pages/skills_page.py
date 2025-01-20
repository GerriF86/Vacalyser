import streamlit as st
from utils import *
from config import *

def main():
    st.header(f"Skills for {st.session_state.role_info.get('job_title', '')}")
    job_title = st.session_state.role_info.get("job_title", "")
    st.subheader("Technical Skills")
    # Generiere Technical Skills nur, wenn sie noch nicht aus dem PDF extrahiert wurden oder wenn requested
    if ("pdf_text" in st.session_state and not st.session_state.technical_skills) or st.button("Generate Technical Skills"):
        if job_title:
            with st.spinner("Generating technical skills..."):
                if "pdf_text" in st.session_state:
                    # Extrahiere technische Skills mit RAG
                    extracted_data = extract_data_from_pdf_rag(st.session_state.pdf_text)
                    st.session_state.technical_skills = {skill: {"must_have": False, "nice_to_have": False} for skill in extracted_data.get("required_skills", [])}
                
                # Wenn keine technischen Skills extrahiert werden konnten oder keine PDF-Daten vorhanden sind, generiere mit Llama 3.2
                if not st.session_state.technical_skills:
                    prompt = f"Generate a list of 15 technologies typically required for the job title '{job_title}', in bullet-point format."
                    result = query_ollama(MODEL_NAME, prompt)
                    st.session_state.technical_skills = {skill: {"must_have": False, "nice_to_have": False} for skill in parse_bullet_points(result)}
                
                st.session_state.selected_must_have_technical_skills = []
                st.session_state.selected_nice_to_have_technical_skills = []
        else:
            st.warning("Please enter a job title.")
    if "technical_skills" in st.session_state:
        for skill, skill_data in st.session_state.technical_skills.items():
            col1, col2 = st.columns(2)
            with col1:
                if st.checkbox(f"Must-have: {skill}", value=skill_data["must_have"], key=f"{skill}_must_have_tech"):
                    skill_data["must_have"] = True
                    if skill not in st.session_state.selected_must_have_technical_skills:
                        st.session_state.selected_must_have_technical_skills.append(skill)
                    skill_data["nice_to_have"] = False
                else:
                    skill_data["must_have"] = False
                    if skill in st.session_state.selected_must_have_technical_skills:
                        st.session_state.selected_must_have_technical_skills.remove(skill)
            with col2:
                if st.checkbox(f"Nice-to-have: {skill}", value=skill_data["nice_to_have"], key=f"{skill}_nice_to_have_tech"):
                    skill_data["nice_to_have"] = True
                    if skill not in st.session_state.selected_nice_to_have_technical_skills:
                        st.session_state.selected_nice_to_have_technical_skills.append(skill)
                    skill_data["must_have"] = False
                else:
                    skill_data["nice_to_have"] = False
                    if skill in st.session_state.selected_nice_to_have_technical_skills:
                        st.session_state.selected_nice_to_have_technical_skills.remove(skill)
        if st.button("Clear Technical Skills Selections", key="clear_tech"):
            for skill in st.session_state.technical_skills:
                st.session_state.technical_skills[skill]["must_have"] = False
                st.session_state.technical_skills[skill]["nice_to_have"] = False
            st.session_state.selected_must_have_technical_skills = []
            st.session_state.selected_nice_to_have_technical_skills = []
    st.subheader("Soft Skills")
    # Generiere Soft Skills nur, wenn sie noch nicht aus dem PDF extrahiert wurden
    if "pdf_text" not in st.session_state or not st.session_state.get("soft_skills"):
        if st.button("Generate Soft Skills"):
            if job_title:
                with st.spinner("Generating soft skills..."):
                    prompt = f"Generate a list of 15 soft skills typically required for the job title '{job_title}', in bullet-point format."
                    result = query_ollama(MODEL_NAME, prompt)
                    st.session_state.soft_skills = {skill: {"must_have": False, "nice_to_have": False} for skill in parse_bullet_points(result)}
                    st.session_state.selected_must_have_soft_skills = []
                    st.session_state.selected_nice_to_have_soft_skills = []
            else:
                st.warning("Please enter a job title.")
    if "soft_skills" in st.session_state:
        for skill, skill_data in st.session_state.soft_skills.items():
            col1, col2 = st.columns(2)
            with col1:
                if st.checkbox(f"Must-have: {skill}", value=skill_data["must_have"], key=f"{skill}_must_have_soft"):
                    skill_data["must_have"] = True
                    if skill not in st.session_state.selected_must_have_soft_skills:
                        st.session_state.selected_must_have_soft_skills.append(skill)
                    skill_data["nice_to_have"] = False
                else:
                    skill_data["must_have"] = False
                    if skill in st.session_state.selected_must_have_soft_skills:
                        st.session_state.selected_must_have_soft_skills.remove(skill)
            with col2:
                if st.checkbox(f"Nice-to-have: {skill}", value=skill_data["nice_to_have"], key=f"{skill}_nice_to_have_soft"):
                    skill_data["nice_to_have"] = True
                    if skill not in st.session_state.selected_nice_to_have_soft_skills:
                        st.session_state.selected_nice_to_have_soft_skills.append(skill)
                    skill_data["must_have"] = False
                else:
                    skill_data["nice_to_have"] = False
                    if skill in st.session_state.selected_nice_to_have_soft_skills:st.session_state.selected_nice_to_have_soft_skills.remove(skill)
        if st.button("Clear Soft Skills Selections", key="clear_soft"):
            for skill in st.session_state.soft_skills:
                st.session_state.soft_skills[skill]["must_have"] = False
                st.session_state.soft_skills[skill]["nice_to_have"] = False
            st.session_state.selected_must_have_soft_skills = []
            st.session_state.selected_nice_to_have_soft_skills = []
    st.write("Selected Must-have Technical Skills:", ", ".join(st.session_state.get("selected_must_have_technical_skills", [])))
    st.write("Selected Nice-to-have Technical Skills:", ", ".join(st.session_state.get("selected_nice_to_have_technical_skills", [])))
    st.write("Selected Must-have Soft Skills:", ", ".join(st.session_state.get("selected_must_have_soft_skills", [])))
    st.write("Selected Nice-to-have Soft Skills:", ", ".join(st.session_state.get("selected_nice_to_have_soft_skills", [])))
    if st.button("Next: Benefits Breakdown"):
        with st.spinner("Identifying attractive benefits..."):
            classic_benefits = ["Health Insurance", "Paid Time Off", "Retirement Plan", "Dental Insurance", "Vision Insurance"]
            innovative_benefits = identify_benefits(st.session_state.role_info.get("job_title", ""))
            st.session_state.benefits = {benefit: {"classic": True, "innovative": False} for benefit in classic_benefits}
            st.session_state.benefits.update({benefit: {"classic": False, "innovative": True} for benefit in innovative_benefits})
            st.session_state.selected_benefits = []
        st.session_state.page = "benefits_page"
        st.rerun()

if __name__ == "__main__":
    main()