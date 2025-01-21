import streamlit as st
from utils import navigate_to_page

def main():
    st.header("Data Extraction Page")

    # Überprüfe, ob Daten extrahiert wurden
    if "pdf_text" in st.session_state:
        st.subheader("Extracted Data:")

        # Zeige die extrahierten Daten an
        st.write(f"**Job Title:** {st.session_state.role_info.get('job_title', 'N/A')}")
        st.write(f"**Company:** {st.session_state.company_info.get('Company Name', 'N/A')}")
        st.write(f"**Location:** {st.session_state.role_info.get('location', 'N/A')}")
        st.write(f"**Extracted Text:**")
        st.write(st.session_state.pdf_text)

        # Weitere Felder anzeigen
        st.write("**Tasks:**")
        if st.session_state.tasks:
            for task in st.session_state.tasks:
                st.write(f"- {task}")
        else:
            st.write("No tasks extracted.")
        
        st.write("**Benefits:**")
        if st.session_state.benefits:
            for benefit in st.session_state.benefits:
                st.write(f"- {benefit}")
        else:
            st.write("No benefits extracted.")

        st.write(f"**Company Description:** {st.session_state.company_info.get('company_description', 'N/A')}")
        
        st.write("**Required Skills:**")
        if st.session_state.role_info["required_skills"]:
            for skill in st.session_state.role_info["required_skills"]:
                st.write(f"- {skill}")
        else:
            st.write("No required skills extracted.")

    else:
        st.subheader("Manually Entered Data")
        # Job Title (already entered on welcome_page)
        st.write(f"Job Title: {st.session_state.role_info['job_title']}")
        # Example for location
        st.session_state.role_info["location"] = st.text_input("Location", value=st.session_state.role_info.get("location", ""), key="location_manual")
        # ... (Add fields for other data to be entered manually)
    if st.button("Next"):
        st.session_state.page = "company_details_page"
        st.rerun()

if __name__ == "__main__":
    main()