# pages/1_welcome_page.py
import streamlit as st
from core_functions import (
    extract_information_from_pdf,
    extract_entities_from_text,
    load_spacy_model,
    scrape_website,
    search_faiss_index,
    create_faiss_index,
    get_relevant_documents
)
from ui_elements import (
    centered_title,
    labeled_text_input,
    labeled_selectbox,
    error_message,
    success_message,
    labeled_radio
)
import time
from error_handling import handle_error
import config
from data_processing import validate_website

# Load the SpaCy model for advanced NLP functions
try:
    nlp = load_spacy_model()
except OSError:
    st.warning(
        "SpaCy model 'de_core_news_sm' not found. Please download it with 'python -m spacy download de_core_news_sm'."
    )
    nlp = None

def main():
    """Functions of the welcome page of the Streamlit application."""

    # Initialize Session State if not present
    st.session_state.setdefault("job_details", {})
    st.session_state.setdefault("company_info", {})
    st.session_state.setdefault("username", "")
    st.session_state.setdefault("current_page", "welcome")
    st.session_state.setdefault("extracted_data", {})

    # Add custom CSS for centering elements
    st.markdown(
        """
        <style>
        .center {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Wrap content in a div with 'center' class for horizontal centering
    st.markdown("<div class='center'>", unsafe_allow_html=True)

    # Basic personalization
    if not st.session_state.username:
        st.session_state.username = st.text_input(
            "Please enter your name:", key="username_input"
        )

    if st.session_state.username:
        centered_title(f"Welcome, {st.session_state.username}!")

    st.image("static/logo.png", use_container_width=True)
    centered_title("Welcome to the Vacancy Fact Finding Analysis Tool!")
    st.markdown(
        "<p style='text-align: center;'>The smart assistant to discover which Requirements your Vacancy really has.</p>",
        unsafe_allow_html=True,
    )

    # --- Early Information Extraction ---
    uploaded_file = st.file_uploader("Upload a PDF job description", type="pdf", key="pdf_uploader")

    if uploaded_file is not None:
        if st.button("Analyze PDF", key="analyze_pdf_button"):
            with st.spinner("Analyzing PDF..."):
                try:
                    st.session_state.extracted_data = extract_information_from_pdf(uploaded_file)
                    time.sleep(1)  # Short pause to show the spinner

                    if st.session_state.extracted_data:
                        # Extract entities with SpaCy if nlp is loaded
                        if nlp:
                            doc = nlp(
                                st.session_state.extracted_data.get("job_title", "")
                                + " "
                                + st.session_state.extracted_data.get("company_name", "")
                                + " "
                                + st.session_state.extracted_data.get("company_location", "")
                            )
                            entities = extract_entities_from_text(doc)

                            # Map entities to corresponding fields
                            if "ORG" in entities:
                                st.session_state.company_info["company_name"] = entities["ORG"][0]
                            if "LOC" in entities:
                                st.session_state.company_info["company_location"] = entities["LOC"][0]
                            if "MISC" in entities:
                                st.session_state.job_details["job_title"] = entities["MISC"][0]

                        success_message("PDF successfully analyzed!")

                        # Automatic mapping of values from PDF analysis
                        st.session_state.job_details.update(st.session_state.extracted_data)

                        # Ask if extracted data should be used
                        st.write(
                            f"We found information about **{st.session_state.extracted_data.get('job_title', 'a position')}** at **{st.session_state.extracted_data.get('company_name', 'a company')}** in **{st.session_state.extracted_data.get('company_location', 'a location')}**."
                        )
                        if st.button("Use this data", key="use_pdf_data_button"):
                            st.rerun()
                    else:
                        error_message(
                            "Error analyzing the PDF file. Please try again or enter the data manually."
                        )
                except Exception as e:
                    handle_error(e, "Error analyzing the PDF file.")

    # Website analysis
    website_url = st.text_input("Enter a website URL for company information (optional):")
    if website_url:
        if st.button("Analyze Website"):
            if validate_website(website_url):
                try:
                    with st.spinner("Analyzing website..."):
                        scraped_info = scrape_website(website_url)
                    if scraped_info:
                        st.session_state.company_info.update(scraped_info)
                        st.write("Website information extracted successfully!")
                        # Extract entities with SpaCy if nlp is loaded and update company_info
                        if nlp:
                            doc = nlp(
                                scraped_info.get("title", "")
                                + " "
                                + " ".join(scraped_info.get("paragraphs", []))
                            )
                            entities = extract_entities_from_text(doc)

                            if "ORG" in entities:
                                st.session_state.company_info["company_name"] = entities["ORG"][0]

                    else:
                        error_message("Error analyzing the website. Please check the URL.")
                except Exception as e:
                    handle_error(e, "Error analyzing website.")
            else:
                st.error("Please enter a valid website URL.")

    # --- Input Fields ---
    # Job Title (conditional based on early extraction)
    if st.session_state.extracted_data.get("job_title"):
        st.info(f"Extracted Job Title: {st.session_state.extracted_data['job_title']}")
        st.session_state.job_details["job_title"] = st.session_state.extracted_data["job_title"]
    else:
        st.session_state.job_details["job_title"] = labeled_text_input(
            "Job Title",
            "job_title_input",
            value=st.session_state.job_details.get("job_title", ""),
            placeholder="Enter the job title (e.g. Data Scientist, Software Engineer)",
            help_text="Enter the job title for the position you want to create or analyze."
        )

    # Job title refinement
    if st.session_state.job_details["job_title"]:
        synonyms = get_job_title_synonyms(st.session_state.job_details["job_title"])
        if synonyms:
            st.session_state.job_details["job_title"] = labeled_radio(
                "Did you mean:",
                [st.session_state.job_details["job_title"]] + synonyms,
                "synonym_radio",
                help_text="Select a similar job title if it matches your intended role better."
            )

    # Role specialization
    if st.session_state.job_details["job_title"]:
        specializations = get_job_specializations(
            st.session_state.job_details["job_title"]
        )
        if specializations:
            selected_specialization = labeled_selectbox(
                "In which area are you looking?",
                ["General"] + specializations,
                "specialization_select",
                help_text="Select a specialization to narrow down the job requirements."
            )
            if selected_specialization != "General":
                st.session_state.job_details[
                    "job_title"
                ] += f" ({selected_specialization})"

    # Job category selection
    st.session_state.job_category = labeled_selectbox(
        "Select the applicable job category (optional):",
        ["General"] + config.FAISS_JOB_CATEGORIES,
        "job_category_select",
        help_text="Selecting a job category can improve search results."
    )

    # Urgency
    st.session_state.job_details["priority"] = labeled_selectbox(
        "How quickly does this position need to be filled?",
        ["Immediately", "Within a month", "In the next 3 months"],
        "priority_select",
        help_text="Indicate the urgency of filling this position."
    )

    # Use existing data
    if st.session_state.job_details["job_title"]:
        faiss_index = create_faiss_index()
        if faiss_index:
            with st.spinner("Searching for similar job descriptions..."):
                results = search_faiss_index(
                    st.session_state.job_details["job_title"], faiss_index
                )
            if results:
                if st.button("Use existing data", key="use_existing_data_button"):
                    # Convert Chroma results to FAISS format and extract metadata
                    metadata = [doc.metadata for doc, _ in results]

                    # Assuming the first result is the most relevant
                    if metadata:
                        st.session_state.job_details.update(metadata[0])
                        success_message("Data from the database loaded!")
                    else:
                        error_message("No metadata found for the selected job description.")

    # Next Page Button removed, navigation is handled in app.py
    if st.button("Proceed to next Page"):
        st.session_state.current_page = "company_details"
        st.rerun()

    # Close the div for centering
    st.markdown("</div>", unsafe_allow_html=True)

# Helper functions for job title refinement and role specialization
def get_job_title_synonyms(job_title):
    """Suggests synonyms or related job titles."""
    synonyms = {
        "data scientist": ["Machine Learning Engineer", "Data Analyst", "AI Specialist"],
        "softwareentwickler": [
            "Software Developer",
            "Programmierer",
            "Software Engineer",
        ],
        # ... Add more synonyms ...
    }
    return synonyms.get(job_title.lower(), [])

def get_job_specializations(job_title):
    """Offers specializations for general job titles."""
    specializations = {
        "softwareentwickler": ["Frontend", "Backend", "Full Stack", "DevOps"],
        # ... Add more specializations ...
    }
    return specializations.get(job_title.lower(), [])

if __name__ == "__main__":
    welcome_page()