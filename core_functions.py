import os
import tempfile
import requests
import spacy
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import Ollama
import streamlit as st
import time
import logging
from error_handling import handle_api_error, handle_error
from data_processing import validate_website
from datetime import datetime, timedelta
import config
import json
import fitz  # PyMuPDF
import faiss
import numpy as np
from bs4 import BeautifulSoup
import random

# Caching Functions
@st.cache_resource()
def load_spacy_model():
    try:
        return spacy.load("de_core_news_sm")
    except OSError:
        logging.warning("SpaCy model 'de_core_news_sm' not found.")
        return None

# Model Configuration
@st.cache_resource
def load_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# FAISS Index Management
@st.cache_resource(hash_funcs={FAISS: lambda _: None})
def create_faiss_index():
    embeddings = load_embeddings()
    if not embeddings:
        st.error("Failed to load embeddings. Check model and dependencies.")
        return None

    index_dir = os.path.join(os.getcwd(), config.INDEX_PATH)

    if os.path.exists(index_dir):
        print(f"Index directory: {index_dir}")
        try:
            faiss_index = FAISS.load_local(
                index_dir,
                embeddings,
                index_name="index",
                allow_dangerous_deserialization=True
            )
            return faiss_index
        except Exception as e:
            st.error(f"Error loading FAISS index: {e}")
            logging.error(f"Error loading FAISS index: {e}")
            return None
    else:
        st.error(f"Index directory does not exist: {index_dir}")
        return None

# PDF Processing
def extract_information_from_pdf(pdf_file):
    text = ""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(pdf_file.getvalue())
            temp_pdf_path = temp_pdf.name

        doc = fitz.open(temp_pdf_path)
        for page in doc:
            text += page.get_text()
        doc.close()
        os.unlink(temp_pdf_path)
    except Exception as e:
        logging.error(f"Error processing PDF: {e}")
    return text

# Search Function (NOT cached)
def search_faiss_index(query: str, faiss_index: FAISS, k: int = 5):
    if faiss_index is None:
        st.error("FAISS index is not initialized.")
        return []
    try:
        results = faiss_index.similarity_search_with_score(query, k=k)
        return results
    except Exception as e:
        st.error(f"Error searching FAISS index: {e}")
        logging.error(f"Error searching FAISS index: {e}")
        return []

# Website Scraping
def scrape_website(url):
    if not validate_website(url):  # Assuming you have this function in data_processing.py
        logging.error("Invalid URL provided.")
        return None

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        return {
            "title": soup.find("title").text.strip() if soup.find("title") else "",
            "paragraphs": [p.text.strip() for p in soup.find_all("p")]
        }
    except Exception as e:
        logging.error(f"Error scraping website: {e}")
        return None

def search_competitor_companies(company_name, industry):
    """Searches for competitor companies in the same industry."""
    # Example implementation using a simple dictionary - replace with your actual logic
    competitors_by_industry = {
        "IT": ["IBM", "Microsoft", "Google", "Amazon", "SAP", "Accenture", "Salesforce", "Oracle", "Adobe", "ServiceNow"],
        "Finance": ["JPMorgan Chase", "Goldman Sachs", "Bank of America", "Citigroup", "Morgan Stanley", "Deutsche Bank", "Credit Suisse", "UBS", "HSBC", "Barclays"],
        "Healthcare": ["Johnson & Johnson", "Pfizer", "Novartis", "Roche", "UnitedHealth Group", "Medtronic", "Abbott Laboratories", "Merck", "Gilead Sciences", "Amgen"],
        "Retail": ["Walmart", "Amazon", "Costco", "Target", "Home Depot", "Tesco", "Carrefour", "Aldi", "Lidl", "IKEA"],
        "Manufacturing": ["Boeing", "General Electric", "3M", "Siemens", "Honeywell", "Caterpillar", "BASF", "Dow Chemical", "DuPont", "Saint-Gobain"],
        "Education": ["Harvard University", "Stanford University", "Massachusetts Institute of Technology (MIT)", "University of Oxford", "University of Cambridge", "University of California, Berkeley", "California Institute of Technology (Caltech)", "Yale University", "Princeton University", "Columbia University"],
        "Energy": ["ExxonMobil", "Royal Dutch Shell", "BP", "Chevron", "TotalEnergies", "Enel", "Duke Energy", "NextEra Energy", "EDF", "Gazprom"],
        "Telecommunication": ["AT&T", "Verizon", "Comcast", "Deutsche Telekom", "Vodafone", "Telefonica", "Orange", "China Mobile", "Nippon Telegraph and Telephone (NTT)", "SoftBank"],
        "Automotive": ["Toyota", "Volkswagen", "General Motors", "Ford", "Daimler", "BMW", "Honda", "Hyundai", "Nissan", "Tesla"],
    }

    competitor_companies = competitors_by_industry.get(industry, [])

    # Add some randomness to the selection (optional)
    random.shuffle(competitor_companies)
    return competitor_companies[:5]  # Return up to 5 competitors

@st.cache_data(show_spinner=False)
def estimate_salary_range(job_title, experience_level):
    """Estimates the salary range based on job title and experience level."""
    # Example logic - replace with your actual logic
    base_salary = 0
    if "data scientist" in job_title.lower():
        base_salary = 80000
    elif "software engineer" in job_title.lower():
        base_salary = 75000
    elif "project manager" in job_title.lower():
        base_salary = 90000
    # ... (further job titles)

    if experience_level == "Junior":
        base_salary *= 0.8
    elif experience_level == "Senior":
        base_salary *= 1.2
    elif experience_level == "Lead":
        base_salary *= 1.5
    # ... (further experience levels)

    lower_bound = int(base_salary * 0.9)
    upper_bound = int(base_salary * 1.1)

    return f"{lower_bound}-{upper_bound}"

def extract_entities_from_text(doc):
    """
    Extrahiert benannte Entitäten aus einem SpaCy-Dokument.
    """
    entities = {}
    for ent in doc.ents:
        if ent.label_ not in entities:
            entities[ent.label_] = []
        entities[ent.label_].append(ent.text)
    return entities

# Function to generate text with Ollama and the new model
def generate_text_with_ollama(prompt, model_name=config.MODEL_NAME, ollama_url=config.OLLAMA_URL):
    """Generates text with a local language model via the Ollama API."""
    try:
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False  # Disable streaming to get the full response
        }
        headers = {"Content-Type": "application/json"}

        response = requests.post(ollama_url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()  # Raises an exception if the status code indicates an error

        response_json = response.json()
        generated_text = response_json.get("response", "").strip()
        return generated_text
    except requests.exceptions.RequestException as e:
        handle_api_error(e, "Ollama")
        return ""
    except Exception as e:
        handle_error(e, "Error generating text with Ollama.")
        return ""

# Replace the functions generate_text_with_openai and generate_text_with_claude with the new function
def generate_text(prompt):
    return generate_text_with_ollama(prompt)

def get_department_keywords(department):
    """Suggests context-specific keywords based on the selected department."""
    if department == "IT":
        return [
            "Cloud",
            "DevOps",
            "Security",
            "Agile",
            "Big Data",
            "AI",
            "Machine Learning",
            "Cybersecurity",
            "Software Development",
            "Network",
            "Database",
            "Frontend",
            "Backend",
            "Full Stack",
            "Mobile Development",
            "IoT",
            "Blockchain",
            "Virtualization",
        ]
    elif department == "Marketing":
        return [
            "Digital Marketing",
            "SEO",
            "SEM",
            "Social Media",
            "Content Marketing",
            "Branding",
            "Campaign Management",
            "Analytics",
            "Market Research",
            "Email Marketing",
            "Public Relations",
            "Event Management",
            "Marketing Automation",
        ]
    # ... (other departments and keywords)
    else:
        return []

def estimate_team_size(department_size):
    """Suggests a typical team size based on the department size."""
    if department_size < 10:
        return 3
    elif department_size < 30:
        return 5
    elif department_size < 50:
        return 8
    elif department_size < 100:
        return 10
    else:
        return 15

def get_index_for_value(value, options):
    """
    Returns the index of a value in a list of options.
    """
    try:
        return options.index(value)
    except ValueError:
        return 0

def get_contract_type_suggestions(job_title, industry):
    """Suggests industry-standard contract types for the role."""
    if industry == "IT":
        if (
            "freelance" in job_title.lower()
            or "contractor" in job_title.lower()
        ):
            return ["Freelance", "Contract", "Temporary"]
        else:
            return ["Permanent", "Contract", "Internship", "Part-time"]
    elif industry == "Finance":
        return ["Permanent", "Contract", "Temporary"]
    # ... (further industries and suggestions)
    else:
        return ["Permanent", "Part-time", "Temporary", "Contract"]

def get_work_model_suggestion(job_location):
    """Suggests a suitable working model (Onsite, Remote, Hybrid) based on the location and industry."""
    # Example logic based on job location
    if "Berlin" in job_location or "Munich" in job_location:
        return "Hybrid"
    elif "Remote" in job_location:
        return "Remote"
    else:
        return "Onsite"

def estimate_travel_percentage(travel_requirements):
    """Suggests a typical percentage of travel time based on the travel requirements."""
    if (
        "häufig" in travel_requirements.lower()
        or "regelmäßig" in travel_requirements.lower()
    ):
        return 50
    elif "gelegentlich" in travel_requirements.lower():
        return 25
    elif "selten" in travel_requirements.lower():
        return 10
    else:
        return 0

def suggest_max_experience(min_experience):
    """Suggests a suitable maximum experience level range."""
    if min_experience < 2:
        return 5
    elif min_experience < 5:
        return 8
    elif min_experience < 10:
        return 12
    else:
        return 15

def suggest_language_levels(languages):
    """Suggests a typical language level for the selected languages."""
    language_levels = {}
    for language in languages.split(","):
        language = language.strip()
        if language.lower() == "deutsch":
            language_levels[language] = "C2"  # Native speaker/near-native proficiency
        elif language.lower() == "englisch":
            language_levels[language] = "C1"  # Proficient
        else:
            language_levels[language] = "B2"  # Fluent in speech and writing
    return language_levels

def suggest_certifications(technical_skills):
    """Suggests relevant certifications for the selected technical skills."""
    certifications = []
    for skill in technical_skills.split(","):
        skill = skill.strip().lower()
        if skill == "python":
            certifications.extend(
                [
                    "PCAP – Certified Associate in Python Programming",
                    "PCEP – Certified Entry-Level Python Programmer",
                ]
            )
        elif skill == "java":
            certifications.extend(
                [
                    "Oracle Certified Associate, Java SE 8 Programmer",
                    "Oracle Certified Professional, Java SE 11 Developer",
                ]
            )
        elif skill == "aws":
            certifications.extend(
                [
                    "AWS Certified Solutions Architect – Associate",
                    "AWS Certified Developer – Associate",
                ]
            )
        # ... (further skills and certifications)
    return list(set(certifications))  # Remove duplicates

def get_tasks_for_job_title(job_title):
    """Retrieves predefined tasks for a given job title."""
    # Example data - replace with your actual data source
    tasks_data = {
        "Software Engineer": [
            "Develop and maintain software applications",
            "Write clean, efficient, and testable code",
            "Conduct code reviews",
            "Collaborate with team members on design and architecture",
            "Troubleshoot and debug software issues",
            "Participate in agile development processes",
        ],
        "Data Scientist": [
            "Analyze large datasets to extract insights",
            "Develop and implement machine learning models",
            "Conduct statistical analyses",
            "Create data visualizations and reports",
            "Communicate findings to stakeholders",
            "Stay updated on the latest data science techniques",
        ],
        # Add more job titles and tasks as needed
    }
    return tasks_data.get(job_title, [])

def get_competitor_benefits(competitor_companies):
    """Retrieves the benefits of competitor companies (Example - would need to be implemented with actual data source)."""
    # Here one could implement e.g. a database query or web scraping
    competitor_benefits = {
        "Competitor A": [
            "Company Pension Scheme",
            "Flexible Working Hours",
            "Home Office",
        ],
        "Competitor B": [
            "Health Insurance",
            "Training Opportunities",
            "Company Car",
        ],
        "Competitor C": ["Stock Options", "Profit Sharing", "Sabbatical"],
    }
    return competitor_benefits

def get_job_specific_benefits(job_title):
    """Suggests benefits that are particularly relevant for the specific position."""
    job_specific_benefits = {
        "Softwareentwickler": [
            "Latest Technologies",
            "Hackathons",
            "Conference Visits",
        ],
        "Data Scientist": [
            "Access to large amounts of data",
            "High-Performance Computing",
            "Research Projects",
        ],
        "Projektmanager": ["Certification Courses (e.g. PMP)", "Mentoring Programs"],
        # ... (further job titles and benefits)
    }

    # Search the keys for matches with the job title
    for title, benefits in job_specific_benefits.items():
        if title.lower() in job_title.lower():
            return benefits
    return []

def get_regional_benefits(job_location):
    """Displays regional differences in benefits that are particularly relevant or appreciated in the respective region."""
    regional_benefits = {
        "Berlin": ["Start-up Culture", "International Teams", "Language Courses"],
        "München": [
            "High Quality of Life",
            "Near the Alps",
            "Strong in Research and Development",
        ],
        "Hamburg": ["Maritime Flair", "Media-rich", "Good Work-Life Balance"],
        # ... (further regions and benefits)
    }

    # Search the keys for matches with the job location
    for location, benefits in regional_benefits.items():
        if location.lower() in job_location.lower():
            return benefits
    return []

def estimate_benefit_costs(selected_benefits):
    """Provides a (rough) cost-benefit analysis of the selected benefits."""
    # Example costs per benefit (per year per employee)
    benefit_costs = {
        "Company Pension Scheme": 1000,
        "Health Insurance": 500,
        "Flexible Working Hours": 100,
        "Home Office Options": 200,
        "Training Opportunities": 800,
        "Company Car": 5000,
        "Meal Allowance": 300,
        "Employee Discounts": 100,
        "Sport- und Fitnessangebote": 300,
        "Company Kindergarten": 2000,
        "Sabbatical Options": 1500,
        "Workation Opportunities": 1000,
        "Mental Health Support": 400,
        "Pet-friendly Workplace": 50,
        "Volunteer Days": 150,
        "Stock Options": 2000,
        "Profit Sharing": 1000,
        "Environmentally Friendly Mobility Solutions (e.g. Job Bike)": 400,
        "Paid Parental Leave": 1200,
        "Public Transport Ticket": 600,
        "Lifelong Learning Budget": 700,
        "Free Snacks and Drinks": 250,
        "On-site Gym": 1000,
        "Wellness Programs": 350,
    }
    total_cost = 0
    for benefit in selected_benefits:
        total_cost += benefit_costs.get(benefit, 0)  # If costs are unknown, assume 0
    return total_cost

@st.cache_data(ttl=timedelta(days=1))
def update_data_periodically():
    """
    Example function to periodically update data.
    Simulates an update with a short pause and a log output.
    """
    try:
        with st.spinner("Updating data..."):
            # Replace this with your actual data update logic
            # For example, you could fetch data from a database or API here
            # and update the FAISS index or other data structures.
            # For now, it's just a placeholder.

            # Example: Reload FAISS index
            # faiss_index = create_faiss_index()
            # if faiss_index:
            #     st.session_state.faiss_index = faiss_index

            logging.info("Data successfully updated.")

    except Exception as e:
        handle_error(e, "Error updating data")

# Initialize a dummy RAG chain for demonstration purposes
def initialize_rag_chain():
    if "rag_chain" not in st.session_state:
        print("Initializing RAG chain...")
        try:
            embeddings = load_embeddings()
            index_dir = os.path.join(os.getcwd(), config.INDEX_PATH)
            
            if os.path.exists(index_dir):
                faiss_index = FAISS.load_local(
                    index_dir,
                    embeddings,
                    index_name="index",
                    allow_dangerous_deserialization=True
                )
                retriever = faiss_index.as_retriever(search_kwargs={"k": 3})
                llm = Ollama(model=config.MODEL_NAME, base_url=config.OLLAMA_URL)
                rag_chain = RetrievalQA.from_chain_type(
                    llm=llm,
                    chain_type="stuff",
                    retriever=retriever,
                    return_source_documents=True
                )

                st.session_state.rag_chain = rag_chain
                print("RAG chain initialized and stored in session state.")
            else:
                print(f"Index directory does not exist: {index_dir}")
        except Exception as e:
            print(f"Failed to initialize RAG chain: {e}")

# Call the initialization function at the start of the application
initialize_rag_chain()

# Updated function to use FAISS for document retrieval and RAG
def extract_data_from_pdf_rag(pdf_file):
    # Extrahiere Text aus PDF
    text = extract_text_from_pdf_pypdf2(pdf_file)
    if not text:
        print("Fehler: Konnte Text nicht aus PDF extrahieren.")
        return {}

    # Extrahiere zusätzliche Felder mit Regex
    extracted_fields = extract_additional_fields_from_pdf_text(text)

    # Initialisiere die Ollama RAG-Kette, falls noch nicht geschehen
    if 'rag_chain' not in st.session_state:
        initialize_rag_chain()  # Initialisierungsfunktion

    # Verwende die RAG-Kette, um die extrahierten Informationen anzureichern
    rag_results = {}

    # Hole die relevanten Dokumente basierend auf dem Jobtitel aus dem FAISS-Index
    job_title = extracted_fields.get('job_title', '')
    relevant_docs = get_relevant_documents(query=job_title, n_results=3)

    # Erstelle einen RAG-Prompt mit den relevanten Dokumenten
    rag_prompt = rag_enhanced_query(
        query=f"Welche Aufgaben und Verantwortlichkeiten beinhaltet die Rolle {job_title}?",
        context_documents=relevant_docs
    )

    rag_results['tasks'] = query_ollama(config.MODEL_NAME, rag_prompt)

    rag_prompt = rag_enhanced_query(
        query=f"Welche Fähigkeiten sind für die Rolle {job_title} erforderlich?",
        context_documents=relevant_docs
    )
    rag_results['required_skills'] = query_ollama(config.MODEL_NAME, rag_prompt)

    rag_prompt = rag_enhanced_query(
        query=f"Welche Zusatzleistungen werden typischerweise für die Rolle {job_title} angeboten?",
        context_documents=relevant_docs
    )
    rag_results['benefits'] = query_ollama(config.MODEL_NAME, rag_prompt)

    # Kombiniere extrahierte Felder und RAG-Ergebnisse
    extracted_data = {**extracted_fields, **rag_results}

    return extracted_data

def query_rag_chain(query):
    if 'rag_chain' in st.session_state:
        # Ensure the question is correctly formatted, e.g., as a complete sentence
        if not query.endswith("?"):
            query += "?"
        # Use the chain in a way that accesses the correct attributes
        try:
            response = st.session_state.rag_chain.invoke(query)
            # Check if response is a dictionary and has 'result' key
            if isinstance(response, dict) and 'result' in response:
                return response['result']
            else:
                logging.error("RAG response does not contain 'result' key.")
                return "Response format is not as expected."
        except Exception as e:
            logging.error(f"Error querying RAG chain: {e}")
            return f"An error occurred: {e}"
    else:
        logging.error("RAG chain is not initialized.")
        return "RAG chain is not initialized."
    
def get_relevant_documents(query, n_results=3):
    """Retrieves relevant documents from the FAISS index based on a query."""
    faiss_index, metadata = load_faiss_index()

    if faiss_index is None or not metadata:
        st.warning("FAISS index or metadata not loaded.")
        return []

    # Convert the query to a vector using the same embedding model
    embedding_model = load_embeddings()
    query_vector = np.array(embedding_model.embed_query(query)).reshape(1, -1)

    # Perform the search in the FAISS index
    distances, indices = faiss_index.search(query_vector, n_results)

    relevant_documents = []
    for i in indices[0]:
        if i < len(metadata):
            relevant_documents.append(metadata[i]['job_description'])
        else:
            print(f"Index {i} is out of bounds.")
    return relevant_documents

def rag_enhanced_query(query, context_documents):
    """Creates an enhanced query for the RAG model by combining the original query with context from relevant documents."""
    context_string = " ".join(context_documents)
    enhanced_query = f"""
    Based on the following context:
    ---
    {context_string}
    ---
    Answer the following question:
    {query}
    """
    return enhanced_query

if __name__ == "__main__":
    # Perform the update once at startup (or in a separate script,
    # which is executed regularly)
    update_data_periodically()

    # Note: For regular execution in the background, you could use a scheduler like APScheduler.
    # from apscheduler.schedulers.background import BackgroundScheduler
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(update_data_periodically, 'interval', days=1) # Run the update daily
    # scheduler.start()