import streamlit as st
from utils import styled_button, get_relevant_documents, rag_enhanced_query, parse_bullet_points, query_ollama

# --- RAG Functions ---
def get_company_info(company_name):
    relevant_docs = get_relevant_documents(
        query=f"Informationen über das Unternehmen {company_name}",
        n_results=2
    )
    rag_prompt = rag_enhanced_query(
        query=f"""
        Provide information about {company_name}:
        - Industry
        - Company Location
        - Company Size
        - Website
        """,
        context_documents=relevant_docs
    )
    response = query_ollama(MODEL_NAME, rag_prompt)

    info = {}
    lines = response.split("\n")
    for line in lines:
        if "-" in line:
            key, value = line.split("-", 1)
            key = key.strip()
            value = value.strip()
            if key.lower() == "industry":
                info["industry"] = value
            elif key.lower() == "company location":
                info["company_location"] = value
            elif key.lower() == "company size":
                info["company_size"] = value.lower()
            elif key.lower() == "website":
                info["website"] = value

    return info

def main():
    # Seitentitel
    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            <div style='color: #696969; font-size: 2em; font-weight: 700; line-height: 1.2; text-align: left;'>Company Details</div>
        </div>
        """,
        unsafe_allow_html=True
    )

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
        "**Company Size**", options=employee_ranges, value="1-10"
    )

    st.session_state.company_info["Department Employees"] = st.number_input(
        label="Department Size",
        min_value=0,
        max_value=1000,
        value=0,
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
    try:
        default_industry_index = top_industries.index(st.session_state.company_info["Industry"])
    except ValueError:
        default_industry_index = 0

    st.session_state.company_info["Industry"] = st.selectbox(
        "Industry", options=top_industries, index=default_industry_index
    )

    st.session_state.company_info["Website"] = st.text_input("Website", value=st.session_state.company_info["Website"])

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

    # Button Layout anpassen
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("Next: Department Info"):
            st.session_state.page = "department_info_page"
            st.rerun()