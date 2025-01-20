import streamlit as st
from utils import extract_text_from_pdf_pypdf2, extract_data_from_pdf_rag

def main():
    job_title = st.session_state.role_info["job_title"]
    st.header(f"Benefits for {job_title}")
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
    manual_benefit = st.text_input(label="Add a custom benefit:", placeholder="e.g., Pet insurance")
    if manual_benefit:
        st.session_state.benefits[manual_benefit] = {"classic": False, "innovative": False}
        st.session_state.selected_benefits.append(manual_benefit)
    st.write("Selected Benefits:", ", ".join(st.session_state.selected_benefits))
    if st.button("Next: Recruitment Roadmap"):
        st.session_state.page = "recruitment_process_page"
        st.rerun()

if __name__ == "__main__":
    main()