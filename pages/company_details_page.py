import streamlit as st
from utils import get_company_info, navigate_to_page

def main():
    company_name = st.session_state.get("company_info", {}).get("Company Name", "the company")
    job_title = st.session_state.role_info["job_title"]
    st.header("Tell us about the Company")
    st.subheader(f"Setting the stage for: {job_title} at {company_name}")
    st.subheader("Company Vitals")
    st.session_state.company_info["Company Name"] = st.text_input(
        label="Company Name",
        value=st.session_state.company_info["Company Name"],
        placeholder="e.g., Acme Corp"
    )
    if st.session_state.company_info["Company Name"] and st.button("Autofill Company Intel", key="autofill"):
        with st.spinner("Scouring the web for company info..."):
            retrieved_info = get_company_info(st.session_state.company_info["Company Name"])
            for key, value in retrieved_info.items():
                if key in st.session_state.company_info:
                    st.session_state.company_info[key] = value
    st.session_state.company_info["Company Location"] = st.text_input(
        label="Company Location", value=st.session_state.company_info["Company Location"], placeholder="e.g., Silicon Valley, CA"
    )
    employee_ranges = ["1-10", "11-50", "51-100", "101-250", "251-500", "501-1000", "1001-5000", "5000+"]
    st.session_state.company_info["Company Size"] = st.select_slider(
        "**Company Size**", options=employee_ranges, value=st.session_state.company_info.get("Company Size", "1-10")
    )
    st.session_state.company_info["Department Employees"] = st.number_input(
        label="Department Size",
        min_value=0,
        max_value=1000,
        value=st.session_state.company_info.get("Department Employees", 0),
        step=1,
        key="department_employees",
    )
    top_industries = [
        "Automotive",
        "Education",
        "Energy",
        "Finance",
        "Healthcare",
        "Hospitality",
        "Manufacturing",
        "Other",
        "Retail",
        "Tech",
        "Telecom",
    ]
    
    st.session_state.company_info["Industry"] = st.selectbox(
    "Industry", options=top_industries, index=top_industries.index(st.session_state.company_info["Industry"]) if st.session_state.company_info.get("Industry") in top_industries else 0
)
    st.session_state.company_info["Website"] = st.text_input("Website", value=st.session_state.company_info.get("Website", ""))
    st.subheader("Company Culture")
    culture_options = [
        "innovativ",
        "dynamisch",
        "teamorientiert",
        "kundenorientiert",
        "ergebnisorientiert",
        "mitarbeiterorientiert",
        "nachhaltig",
        "flexibel",
        "traditionsbewusst",
        "international",
        "familiär",
        "wachstumsorientiert",
        "qualitätsorientiert",
        "sozial verantwortlich",
        "lernend"
    ]
    st.session_state.company_info["Unternehmenskultur"] = st.multiselect(
        "Unternehmenskultur",
        options=culture_options,
        default=st.session_state.company_info.get("Unternehmenskultur", []),
    )
    if st.button("Next: Dive into the Role"):
        st.session_state.page = "job_details_page"
        st.rerun()

if __name__ == "__main__":
    main()