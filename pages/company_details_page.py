# pages/2_company_details_page.py
import streamlit as st
from core_functions import (
    scrape_website,
    extract_entities_from_text,
    load_spacy_model,
    get_index_for_value,
    search_competitor_companies
)
import concurrent.futures
from ui_elements import (
    centered_title,
    labeled_text_input,
    labeled_selectbox,
    labeled_slider,
    labeled_multiselect,
    section_title,
    success_message,
)
from error_handling import handle_error, handle_api_error
from data_processing import validate_website
import config

# Load the SpaCy model for advanced NLP functions
try:
    nlp = load_spacy_model()
except OSError:
    st.warning(
        "SpaCy model 'de_core_news_sm' not found. Please download it with 'python -m spacy download de_core_news_sm'."
    )
    nlp = None

def main():
    """Functions of the company details page of the Streamlit application."""
    centered_title("Company Details")

    # Initialize Session State if not existing
    if "company_info" not in st.session_state:
        st.session_state.company_info = {}

    # Autofill button
    if st.button("Autofill Company Intel"):
        st.session_state.company_info = autofill_company_details(
            st.session_state.company_info
        )

    # Input fields with improved logic and suggestions from ui_elements.py
    st.session_state.company_info["company_name"] = labeled_text_input(
        "Company Name",
        "company_name",
        value=st.session_state.company_info.get("company_name", ""),
        help_text="The name of the company",
    )

    st.session_state.company_info["company_location"] = labeled_text_input(
        "Location",
        "company_location",
        value=st.session_state.company_info.get("company_location", ""),
        help_text="The main location of the company",
    )

    st.session_state.company_info["company_size"] = labeled_slider(
        "Company Size",
        1,
        1000,
        "company_size",
        value=st.session_state.company_info.get("company_size", 1),
        step=1,
        help_text="The approximate number of employees in the company",
    )

    # Company size refinement with select slider for mobile devices
    if "company_size" in st.session_state.company_info:
        detailed_size_options = get_detailed_size_options(
            st.session_state.company_info["company_size"]
        )
        if detailed_size_options:
            st.session_state.company_info["company_size"] = labeled_slider(
                "Can you specify the company size more precisely?",
                detailed_size_options[0],
                detailed_size_options[-1],
                "detailed_size",
                value=st.session_state.company_info["company_size"],
                step=1,
                help_text="More precise specification of the number of employees",
            )

    # Industry selection
    st.session_state.company_info["industry"] = labeled_selectbox(
        "Industry",
        [
            "",
            "IT",
            "Finance",
            "Healthcare",
            "Retail",
            "Manufacturing",
            "Education",
            "Energy",
            "Telecommunication",
            "Automotive",
        ],
        "industry",
        index=get_index_for_value(
            st.session_state.company_info.get("industry"),
            [
                "",
                "IT",
                "Finance",
                "Healthcare",
                "Retail",
                "Manufacturing",
                "Education",
                "Energy",
                "Telecommunication",
                "Automotive",
            ],
        ),
        help_text="The industry in which the company operates",
    )

    # Industry-specific culture with improved display
    if st.session_state.company_info["industry"]:
        suggested_culture_traits = get_industry_culture_traits(
            st.session_state.company_info["industry"]
        )
        if suggested_culture_traits:
            section_title("Company Culture")

            # Ensure that suggested_culture_traits is a list
            if not isinstance(suggested_culture_traits, list):
                suggested_culture_traits = [suggested_culture_traits]

            # Ensure that st.session_state.company_info["company_culture"] is initialized as a list
            if "company_culture" not in st.session_state.company_info:
                st.session_state.company_info["company_culture"] = []

            # Combine suggested_culture_traits and current_culture_traits, removing duplicates
            all_traits = list(set(suggested_culture_traits + st.session_state.company_info["company_culture"]))

            st.session_state.company_info["company_culture"] = labeled_multiselect(
                f"Which of these characteristics common in the {st.session_state.company_info['industry']} industry apply to the company culture?",
                all_traits,
                "industry_culture_traits",
                default=st.session_state.company_info.get("company_culture", []),
                help_text="Cultural characteristics that are typical for the industry and the company",
            )

    # Website analysis
    st.session_state.company_info["website"] = labeled_text_input(
        "Website",
        "website",
        value=st.session_state.company_info.get("website", ""),
        help_text="The website of the company (e.g. www.example.com)",
    )
    if st.session_state.company_info["website"]:
        if st.button("Analyze Website"):
            if validate_website(st.session_state.company_info["website"]):
                try:
                    with st.spinner("Analyzing website..."):
                        scraped_info = scrape_website(
                            st.session_state.company_info["website"]
                        )
                    if scraped_info:
                        st.write(
                            "We found the following information on the website:"
                        )
                        for key, value in scraped_info.items():
                            st.write(f"- **{key.capitalize()}**: {value}")

                        # Extract entities with SpaCy if nlp is loaded
                        if nlp:
                            doc = nlp(
                                scraped_info.get("title", "")
                                + " "
                                + " ".join(scraped_info.get("paragraphs", []))
                            )
                            entities = extract_entities_from_text(doc)

                            # Assign entities to corresponding fields
                            if "ORG" in entities:
                                st.session_state.company_info["company_name"] = entities[
                                    "ORG"
                                ][0]

                        if st.button("Use Information"):
                            st.session_state.company_info.update(scraped_info)
                            success_message("Information successfully übernommen!")

                except Exception as e:
                    handle_error(e, "Error analyzing website.")
            else:
                st.error("Please enter a valid website URL.")

    # Manual input of company culture
    if "company_culture" not in st.session_state.company_info:
        st.session_state.company_info["company_culture"] = []

    # Multiselect widget for selecting suggested culture traits
    st.session_state.company_info["company_culture"] = labeled_multiselect(
        "Company Culture",
        [
            "Innovative",
            "Team-oriented",
            "Customer-oriented",
            "Results-oriented",
            "Sustainable",
            "Diverse",
        ],
        "company_culture",
        default=st.session_state.company_info.get("company_culture", []),
        help_text="Select the applicable characteristics of the company culture",
    )

    # Dynamic culture selection
    if st.session_state.company_info["company_culture"]:
        additional_culture_traits = get_dynamic_culture_traits(
            st.session_state.company_info["company_culture"]
        )
        if additional_culture_traits:
            selected_additional_traits = labeled_multiselect(
                "The following often match the selected cultural characteristics:",
                additional_culture_traits,
                "additional_culture_traits",
                default=[],
                help_text="Select additional matching cultural characteristics",
            )
            st.session_state.company_info["company_culture"].extend(
                selected_additional_traits
            )
            st.session_state.company_info["company_culture"] = list(
                set(st.session_state.company_info["company_culture"])
            )

   # Competitor analysis (concurrent execution)
    if st.session_state.company_info["company_name"] and st.session_state.company_info["industry"]:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(
                search_competitor_companies,
                st.session_state.company_info["company_name"],
                st.session_state.company_info["industry"]
            )
            try:
                # Get the result of the future, with a timeout to prevent indefinite waiting
                competitor_companies = future.result(timeout=60)  # Timeout after 60 seconds
                st.session_state.company_info["competitor_companies"] = competitor_companies
            except concurrent.futures.TimeoutError:
                st.error("Competitor analysis timed out. Please try again later.")
                logging.error("Competitor analysis timed out.")
            except Exception as e:
                handle_api_error(e, "Competitor analysis")

    if st.button("Next: Department Info"):
        # Validate required fields
        if not st.session_state.company_info["company_name"]:
            st.error("Please enter the company name.")
        elif not st.session_state.company_info["company_location"]:
            st.error("Please enter the company location.")
        elif not st.session_state.company_info["industry"]:
            st.error("Please select an industry.")
        else:
            st.session_state.current_page = "department_info"
            st.rerun()

def get_industry_culture_traits(industry):
    """Suggests industry-specific cultural characteristics."""
    if industry == "IT":
        return [
            "Agile Methods",
            "Remote Work",
            "Open Source",
            "Continuous Learning",
            "Flat Hierarchies",
            "Diversity",
            "Work-Life-Balance",
            "Result-oriented",
            "Informal",
            "Technology-driven",
        ]
    elif industry == "Finance":
        return [
            "Performance-oriented",
            "Competitive",
            "Compliant",
            "Traditional",
            "Numbers-driven",
            "Hierarchical",
            "Risk-conscious",
            "Customer-oriented",
            "Formal",
            "Process-oriented",
        ]
    elif industry == "Healthcare":
        return [
            "Patient-oriented",
            "Ethical",
            "Regulated",
            "Team-oriented",
            "Scientific",
            "Innovative",
            "Careful",
            "Responsible",
        ]
    elif industry == "Retail":
        return [
            "Customer-oriented",
            "Sales-oriented",
            "Fast-paced",
            "Trend-conscious",
            "Competitive",
            "Flexible",
            "Hands-on",
        ]
    elif industry == "Manufacturing":
        return [
            "Production-oriented",
            "Efficient",
            "Safety-conscious",
            "Quality-oriented",
            "Process-oriented",
            "Hierarchical",
            "Technology-driven",
        ]
    elif industry == "Education":
        return [
            "Knowledge-oriented",
            "Collaborative",
            "Innovative",
            "Pedagogical",
            "Research-oriented",
            "Social",
            "Development-oriented",
        ]
    elif industry == "Energy":
        return [
            "Sustainable",
            "Environmentally conscious",
            "Innovative",
            "Safety-conscious",
            "Regulated",
            "Long-term",
            "Technology-driven",
        ]
    elif industry == "Telecommunication":
        return [
            "Technology-driven",
            "Innovative",
            "Fast-paced",
            "Customer-oriented",
            "Connected",
            "Competitive",
            "Regulated",
        ]
    elif industry == "Automotive":
        return [
            "Engineering-driven",
            "Innovative",
            "Quality-oriented",
            "Traditional",
            "Process-oriented",
            "Competitive",
            "Global",
        ]
    else:
        return []

def autofill_company_details(company_info):
    """
    Attempts to automatically fill in company details based on existing information.

    Args:
        company_info (dict): A dictionary containing the previously known company information.

    Returns:
        dict: An updated dictionary containing the company information.
    """
    # Use information from the PDF analysis if available
    if "extracted_data" in st.session_state:
        extracted_data = st.session_state.extracted_data
        if "company_name" in extracted_data:
            company_info["company_name"] = extracted_data["company_name"]
        if "company_location" in extracted_data:
            company_info["company_location"] = extracted_data["company_location"]
        # ... (further assignments if available) ...

    # If a website is available, try to scrape it
    if "website" in company_info:
        scraped_data = scrape_website(company_info["website"])
        if scraped_data:
            company_info.update(scraped_data)

    return company_info

def get_detailed_size_options(company_size_range):
    """
    Provides more detailed selection options for the company size based on the initial selection.

    Args:
        company_size_range (int): The approximate company size.

    Returns:
        list: A list with more detailed size specifications or None if no refinement is available.
    """
    if company_size_range <= 10:
        return [1, 5, 10]  # More detailed options for the range 1-10
    elif company_size_range <= 50:
        return [11, 25, 50]  # More detailed options for the range 11-50
    elif company_size_range <= 200:
        return [51, 100, 200]  # More detailed options for the range 51-200
    elif company_size_range <= 500:
        return [201, 350, 500]
    elif company_size_range <= 1000:
        return [501, 750, 1000]
    else:
        return [1000]

def get_dynamic_culture_traits(selected_traits):
    """Suggests additional matching attributes based on the selected cultural characteristics."""
    suggestions = {
        "Innovative": ["Creative", "Open to new ideas", "Experimental", "Visionary"],
        "Team-oriented": ["Collaborative", "Cooperative", "Supportive", "Communicative"],
        "Customer-oriented": ["Service-oriented", "Empathetic", "Responsive", "Client-focused"],
        "Results-oriented": ["Ambitious", "Performance-driven", "Goal-oriented", "Efficient"],
        "Sustainable": ["Environmentally conscious", "Socially responsible", "Ethical", "Long-term oriented"],
        "Diverse": ["Inclusive", "Multicultural", "Open-minded", "Respectful"],
        "Agile Methods": ["Flexible", "Adaptable", "Iterative", "Scrum-based"],
        "Remote Work": ["Distributed", "Virtual", "Independent", "Self-organized"],
        "Open Source": ["Community-driven", "Transparent", "Collaborative", "Open-minded"],
        "Continuous Learning": ["Curious", "Growth-oriented", "Development-focused", "Adaptive"],
        "Flat Hierarchies": ["Non-hierarchical", "Egalitarian", "Empowered", "Autonomous"], "Diversity": ["Inclusive", "Multicultural", "Open-minded", "Respectful"],
        "Work-Life-Balance": ["Flexible", "Family-friendly", "Balanced", "Supportive"],
        "Result-oriented": ["Performance-driven", "Ambitious", "Goal-oriented", "Efficient"],
        "Informal": ["Casual", "Relaxed", "Friendly", "Approachable"],
        "Technology-driven": ["Digital", "Innovative", "Automated", "Data-driven"],
        "Performance-oriented": ["Competitive", "Results-driven", "Ambitious", "Focused"],
        "Competitive": ["Driven", "Ambitious", "Results-oriented", "Market-focused"],
        "Compliant": ["Rule-following", "Structured", "Process-oriented", "Detail-oriented"],
        "Traditional": ["Established", "Conservative", "Hierarchical", "Formal"],
        "Numbers-driven": ["Analytical", "Data-oriented", "Quantitative", "Result-focused"],
        "Hierarchical": ["Structured", "Formal", "Top-down", "Authority-based"],
        "Risk-conscious": ["Cautious", "Conservative", "Analytical", "Security-focused"],
        "Customer-oriented": ["Client-focused", "Service-driven", "Responsive", "Empathetic"],
        "Formal": ["Structured", "Traditional", "Professional", "Ceremonial"],
        "Process-oriented": ["Systematic", "Organized", "Detail-oriented", "Efficient"],
        "Patient-oriented": ["Caring", "Empathetic", "Compassionate", "Service-driven"],
        "Ethical": ["Moral", "Principled", "Responsible", "Value-based"],
        "Regulated": ["Compliant", "Structured", "Controlled", "Standardized"],
        "Team-oriented": ["Collaborative", "Cooperative", "Supportive", "Communicative"],
        "Scientific": ["Analytical", "Research-based", "Evidence-driven", "Methodical"],
        "Innovative": ["Creative", "Experimental", "Open to new ideas", "Visionary"],
        "Careful": ["Thorough", "Detail-oriented", "Precise", "Methodical"],
        "Responsible": ["Accountable", "Conscientious", "Reliable", "Ethical"],
        "Customer-oriented": ["Client-focused", "Service-driven", "Responsive", "Empathetic"],
        "Sales-oriented": ["Result-driven", "Competitive", "Persuasive", "Ambitious"],
        "Fast-paced": ["Dynamic", "Agile", "Flexible", "Time-sensitive"],
        "Trend-conscious": ["Fashionable", "Modern", "Up-to-date", "Market-oriented"],
        "Competitive": ["Driven", "Ambitious", "Results-oriented", "Market-focused"],
        "Flexible": ["Adaptable", "Versatile", "Open to change", "Responsive"],
        "Hands-on": ["Practical", "Pragmatic", "Solution-oriented", "Involved"],
        "Production-oriented": ["Output-focused", "Efficient", "Process-driven", "Quality-conscious"],
        "Efficient": ["Productive", "Streamlined", "Organized", "Time-conscious"],
        "Safety-conscious": ["Cautious", "Risk-averse", "Protective", "Careful"],
        "Quality-oriented": ["Detail-oriented", "Perfectionistic", "High-standard", "Customer-focused"],
        "Process-oriented": ["Systematic", "Organized", "Detail-oriented", "Efficient"],
        "Hierarchical": ["Structured", "Formal", "Top-down", "Authority-based"],
        "Technology-driven": ["Digital", "Innovative", "Automated", "Data-driven"],
        "Knowledge-oriented": ["Learning-focused", "Inquisitive",
         "Research-based", "Expert"],
        "Collaborative": ["Team-oriented", "Cooperative", "Participative", "Inclusive"],
        "Innovative": ["Creative", "Forward-thinking", "Experimental", "Visionary"],
        "Pedagogical": ["Teaching-focused", "Student-centered", "Learning-oriented", "Educational"],
        "Research-oriented": ["Analytical", "Inquisitive", "Scholarly", "Scientific"],
        "Social": ["Community-focused", "Collaborative", "Engaged", "Altruistic"],
        "Development-oriented": ["Growth-focused", "Progressive", "Improvement-driven", "Empowering"],
        "Sustainable": ["Eco-friendly", "Green", "Environmentally responsible", "Long-term focused"],
        "Environmentally conscious": ["Green", "Sustainable", "Eco-friendly", "Responsible"],
        "Innovative": ["Creative", "Forward-thinking", "Experimental", "Visionary"],
        "Safety-conscious": ["Cautious", "Risk-averse", "Protective", "Careful"],
        "Regulated": ["Compliant", "Structured", "Controlled", "Standardized"],
        "Long-term": ["Strategic", "Future-oriented", "Sustainable", "Visionary"],
        "Technology-driven": ["Digital", "Innovative", "Automated", "Data-driven"],
        "Technology-driven": ["Digital", "Innovative", "Automated", "Data-driven"],
        "Innovative": ["Creative", "Forward-thinking", "Experimental", "Visionary"],
        "Fast-paced": ["Dynamic", "Agile", "Flexible", "Time-sensitive"],
        "Customer-oriented": ["Client-focused", "Service-driven", "Responsive", "Empathetic"],
        "Connected": ["Networked", "Integrated", "Interconnected", "Collaborative"],
        "Competitive": ["Driven", "Ambitious", "Results-oriented", "Market-focused"],
        "Regulated": ["Compliant", "Structured", "Controlled", "Standardized"],
        "Engineering-driven": ["Technical", "Analytical", "Problem-solving", "Innovative"],
        "Innovative": ["Creative", "Forward-thinking", "Experimental", "Visionary"],
        "Quality-oriented": ["Detail-oriented", "Perfectionistic", "High-standard", "Customer-focused"],
        "Traditional": ["Established", "Conservative", "Hierarchical", "Formal"],
        "Process-oriented": ["Systematic", "Organized", "Detail-oriented", "Efficient"],
        "Competitive": ["Driven", "Ambitious", "Results-oriented", "Market-focused"],
        "Global": ["International", "Multinational", "Worldwide", "Cross-cultural"],

    }
    selected_traits_lower = [trait.lower() for trait in selected_traits]
    suggested_traits = set()

    for trait, associated_traits in suggestions.items():
        if trait.lower() in selected_traits_lower:
            for associated_trait in associated_traits:
                suggested_traits.add(associated_trait)

    return list(suggested_traits)

if __name__ == "__main__":
    main()