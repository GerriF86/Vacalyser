# pages/8_summary_page.py
import streamlit as st
from fpdf import FPDF
from prompts import (
    generate_job_ad_prompt,
    generate_interview_questions_prompt,
    generate_onboarding_checklist_prompt,
    generate_retention_strategies_prompt,
)
from core_functions import (
    generate_text_with_ollama,
    load_spacy_model,
    get_index_for_value,
)
from data_processing import prepare_data_for_prompt
from ui_elements import centered_title, section_title, labeled_selectbox
from error_handling import handle_error, handle_api_error
import time
import config
from utils import load_system_message


# Load the Spacy model (for text extraction in PDF generation)
nlp = load_spacy_model()

def main():
    """Functions of the summary page of the Streamlit application."""

    centered_title("Summary")

    # Load system messages for different generation tasks
    job_ad_system_message = load_system_message("job_ad")
    interview_questions_system_message = load_system_message("interview_questions")
    onboarding_checklist_system_message = load_system_message("onboarding_checklist")
    retention_strategies_system_message = load_system_message("retention_strategies")

    # Interactive Summary
    st.write("Please review and edit the information below:")
    # First create the tabs
    tabs = st.tabs(
        [
            "Job Details",
            "Company Info",
            "Department Info",
            "Role Info",
            "Skills",
            "Tasks",
            "Recruitment Process",
            "Benefits",
        ]
    )

    # Then insert the content for each tab
    tab_indices = {
        "Job Details": 0,
        "Company Info": 1,
        "Department Info": 2,
        "Role Info": 3,
        "Skills": 4,
        "Tasks": 5,
        "Recruitment Process": 6,
        "Benefits": 7,
    }
    
    with tabs[tab_indices["Job Details"]]:
        with st.expander("Job Details", expanded=True):
            i = 0
            for key, value in st.session_state.job_details.items():
                if key not in [
                    "job_title",
                    "job_category",
                    "department",
                    "department_keywords",
                    "team_size",
                    "reporting_line",
                    "internal_contact",
                    "budget_authority",
                    "hiring_authority",
                    "requisition_originator",
                    "direct_supervisor",
                    "contact_email_hiring",
                    "contact_phone_hiring",
                    "contact_email_requisition",
                    "contact_phone_requisition",
                    "start_date",
                    "contract_type",
                    "job_location",
                    "onsite_percentage",
                    "work_arrangement",
                    "work_model",
                    "travel_requirements",
                    "priority",
                    "training_budget",
                    "salary_range",
                    "vacancy_reason",
                    "experience_level",
                    "required_skills",
                    "experience_level_min_req",
                    "experience_level_max_req",
                    "technical_skills",
                    "experience_level_min_tech",
                    "experience_level_max_tech",
                    "desired_certifications",
                    "education_level",
                    "soft_skills",
                    "experience_level_min_soft",
                    "experience_level_max_soft",
                    "required_languages",
                    "experience_level_min_lang",
                    "experience_level_max_lang",
                    "selected_tasks",
                    "task_frequencies"
                ]:  # Job title already covered on welcome_page
                    if isinstance(value, list):
                        st.session_state.job_details[key] = st.multiselect(
                            f"{key.replace('_', ' ').capitalize()}",
                            options=value,
                            default=value,
                            key=f"summary_{key}_{i}",
                        )
                    elif isinstance(value, str):
                        st.session_state.job_details[key] = st.text_input(
                            f"{key.replace('_', ' ').capitalize()}",
                            value=value,
                            key=f"summary_{key}_{i}",
                        )
                    elif isinstance(value, int):
                        st.session_state.job_details[key] = st.number_input(
                            f"{key.replace('_', ' ').capitalize()}",
                            value=value,
                            key=f"summary_{key}_{i}",
                        )
                    else:
                        st.write(f"{key.replace('_', ' ').capitalize()}: {value}")
                    i += 1

    with tabs[tab_indices["Company Info"]]:
        with st.expander("Company Info", expanded=True):
            i = 0
            for key, value in st.session_state.company_info.items():
                if isinstance(value, list):
                    st.session_state.company_info[key] = st.multiselect(
                        f"{key.replace('_', ' ').capitalize()}",
                        options=value,
                        default=value,
                        key=f"summary_{key}_{i}",
                    )
                elif isinstance(value, str):
                    st.session_state.company_info[key] = st.text_input(
                        f"{key.replace('_', ' ').capitalize()}",
                        value=value,
                        key=f"summary_{key}_{i}",
                    )
                elif isinstance(value, int):
                    st.session_state.company_info[key] = st.number_input(
                        f"{key.replace('_', ' ').capitalize()}",
                        value=value,
                        key=f"summary_{key}_{i}",
                    )
                else:
                    st.write(f"{key.replace('_', ' ').capitalize()}: {value}")
                i += 1

    with tabs[tab_indices["Department Info"]]:
        with st.expander("Department Info", expanded=True):
            i = 0
            for key, value in st.session_state.job_details.items():
                if key in [
                    "department",
                    "department_keywords",
                    "department_size",
                    "team_size",
                    "reporting_line",
                    "internal_contact",
                    "budget_authority",
                    "hiring_authority",
                    "requisition_originator",
                    "direct_supervisor",
                    "contact_email_hiring",
                    "contact_phone_hiring",
                    "contact_email_requisition",
                    "contact_phone_requisition",
                ]:
                    if isinstance(value, list):
                        st.session_state.job_details[key] = st.multiselect(
                            f"{key.replace('_', ' ').capitalize()}",
                            options=value,
                            default=value,
                            key=f"summary_{key}_{i}",
                        )
                    elif isinstance(value, str):
                        st.session_state.job_details[key] = st.text_input(
                            f"{key.replace('_', ' ').capitalize()}",
                            value=value,
                            key=f"summary_{key}_{i}",
                        )
                    elif isinstance(value, int):
                        st.session_state.job_details[key] = st.number_input(
                            f"{key.replace('_', ' ').capitalize()}",
                            value=value,
                            key=f"summary_{key}_{i}",
                        )
                    else:
                        st.write(f"{key.replace('_', ' ').capitalize()}: {value}")
                    i += 1

    with tabs[tab_indices["Role Info"]]:
        with st.expander("Role Info", expanded=True):
            i = 0
            for key, value in st.session_state.job_details.items():
                if key in [
                    "job_title",
                    "start_date",
                    "contract_type",
                    "job_location",
                    "onsite_percentage",
                    "work_arrangement",
                    "work_model",
                    "travel_requirements",
                    "priority",
                    "training_budget",
                    "salary_range",
                    "vacancy_reason",
                    "experience_level",
                ]:
                    if isinstance(value, list):
                        st.session_state.job_details[key] = st.multiselect(
                            f"{key.replace('_', ' ').capitalize()}",
                            options=value,
                            default=value,
                            key=f"summary_{key}_{i}",
                        )
                    elif isinstance(value, str):
                        st.session_state.job_details[key] = st.text_input(
                            f"{key.replace('_', ' ').capitalize()}",
                            value=value,
                            key=f"summary_{key}_{i}",
                        )
                    elif isinstance(value, int):
                        st.session_state.job_details[key] = st.number_input(
                            f"{key.replace('_', ' ').capitalize()}",
                            value=value,
                            key=f"summary_{key}_{i}",
                        )
                    elif isinstance(value, type(None)):  # Überprüfen Sie, ob der Wert None ist
                        st.session_state.job_details[key] = st.text_input(
                            f"{key.replace('_', ' ').capitalize()}",
                            value="",
                            key=f"summary_{key}_{i}",
                        )
                    else:
                        st.write(f"{key.replace('_', ' ').capitalize()}: {value}")
                    i += 1

    with tabs[tab_indices["Skills"]]:
        with st.expander("Skills", expanded=True):
            i = 0
            for key, value in st.session_state.job_details.items():
                if key in [
                    "required_skills",
                    "experience_level_min_req",
                    "experience_level_max_req",
                    "technical_skills",
                    "experience_level_min_tech",
                    "experience_level_max_tech",
                    "desired_certifications",
                    "education_level",
                    "soft_skills",
                    "experience_level_min_soft",
                    "experience_level_max_soft",
                    "required_languages",
                    "experience_level_min_lang",
                    "experience_level_max_lang",
                ]:
                    if isinstance(value, list):
                        st.session_state.job_details[key] = st.multiselect(
                            f"{key.replace('_', ' ').capitalize()}",
                            options=value,
                            default=value,
                            key=f"summary_{key}_{i}",
                        )
                    elif isinstance(value, str):
                        st.session_state.job_details[key] = st.text_area(
                            f"{key.replace('_', ' ').capitalize()}",
                            value=value,
                            key=f"summary_{key}_{i}",
                        )
                    elif isinstance(value, int):
                        st.session_state.job_details[key] = st.number_input(
                            f"{key.replace('_', ' ').capitalize()}",
                            value=value,
                            key=f"summary_{key}_{i}",
                        )
                    else:
                        st.write(f"{key.replace('_', ' ').capitalize()}: {value}")
                    i += 1

    with tabs[tab_indices["Tasks"]]:
        with st.expander("Tasks", expanded=True):
            i = 0
            if "task_frequencies" in st.session_state:
                for task, frequency in st.session_state.task_frequencies.items():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.checkbox(task, key=f"summary_task_{task}_{i}", value=True)
                    with col2:
                        st.session_state.task_frequencies[task] = st.selectbox(
                            "Frequency",
                            options=[
                                "Daily",
                                "Weekly",
                                "Monthly",
                                "Quarterly",
                                "Yearly",
                                "On Demand",
                            ],
                            key=f"summary_freq_{task}_{i}",
                            index=get_index_for_value(
                                frequency,
                                [
                                    "Daily",
                                    "Weekly",
                                    "Monthly",
                                    "Quarterly",
                                    "Yearly",
                                    "On Demand",
                                ],
                            ),
                        )
                    i += 1

    with tabs[tab_indices["Recruitment Process"]]:
        with st.expander("Recruitment Process", expanded=True):
            i = 0
            for step in st.session_state.selected_recruitment_steps:
                st.checkbox(step, key=f"summary_recruitment_{step}_{i}", value=True)
                st.number_input(
                    label=f"Duration of '{step}' (in days)",
                    min_value=0,
                    key=f"summary_duration_{step}_{i}",
                    value=st.session_state.job_details.get(f"duration_{step}", 0),
                )
                st.text_input(
                    label=f"Responsible for '{step}'",
                    key=f"summary_responsible_{step}_{i}",
                    value=st.session_state.job_details.get(f"responsible_{step}", ""),
                )
                i += 1
            st.text_area(
                label="Current Recruitment Process",
                key="summary_current_recruitment_process",
                value=st.session_state.job_details.get(
                    "current_recruitment_process", ""
                ),
            )

    with tabs[tab_indices["Benefits"]]:
        with st.expander("Benefits", expanded=True):
            i = 0
            for benefit in st.session_state.selected_benefits:
                st.checkbox(benefit, key=f"summary_benefit_{benefit}_{i}", value=True)
                i += 1

    # Model selection (Ollama)
    model_choice = labeled_selectbox(
        "Choose an AI Model",
        [config.MODEL_NAME],  # Only show the configured Ollama model
        "model_choice",
        help_text="Select the AI model to be used for text generation."
    )

    # A/B Testing selection
    
    ab_testing_label = "Perform A/B Testing (only for job advertisement)"
    
    ab_testing = st.checkbox(
        label= ab_testing_label,
        key="ab_testing",
        value= False
    )

    # Generate Job Ad
    if st.button("Generate Job Ad"):
        try:
            # Combine the system message and the user prompt
            data_for_prompt = prepare_data_for_prompt(st.session_state)
            prompt = generate_job_ad_prompt(
                data_for_prompt, st.session_state.job_details["job_title"]
            )

            if ab_testing:
                # Generate two variants with different focuses (example)
                prompt_a = prompt + " Focus on the company culture."
                prompt_b = (
                    prompt + " Focus on the technical requirements."
                )

                # Generate with Ollama
                with st.spinner("Generating job advertisement (variant A)..."):
                    generated_job_ad_a = generate_text_with_ollama(prompt_a)
                with st.spinner("Generating job advertisement (variant B)..."):
                    generated_job_ad_b = generate_text_with_ollama(prompt_b)

                st.session_state.generated_job_ad_a = generated_job_ad_a
                st.session_state.generated_job_ad_b = generated_job_ad_b

            else:
                with st.spinner("Generating job advertisement..."):
                    generated_job_ad = generate_text_with_ollama(prompt)

                st.session_state.generated_job_ad = generated_job_ad

        except Exception as e:
            handle_api_error(e, "AI model")
            st.session_state.generated_job_ad = ""
            st.session_state.generated_job_ad_a = ""
            st.session_state.generated_job_ad_b = ""

    # Display the generated job advertisement(s)
    if "generated_job_ad" in st.session_state and st.session_state.generated_job_ad:
        with st.expander("Generated Job Ad", expanded=True):
            st.write(st.session_state.generated_job_ad)

    if (
        "generated_job_ad_a" in st.sessionstate
        and st.session_state.generated_job_ad_a
    ):
        with st.expander("Generated Job Ad (Variant A)", expanded=True):
            st.write(st.session_state.generated_job_ad_a)

    if (
        "generated_job_ad_b" in st.session_state
        and st.session_state.generated_job_ad_b
    ):
        with st.expander("Generated Job Ad (Variant B)", expanded=True):
            st.write(st.session_state.generated_job_ad_b)

    # AI-based optimization suggestions (example)
    if st.button("AI Optimization Suggestions"):
        try:
            with st.spinner(
                "AI optimizes job advertisement and recruitment process..."
            ):
                # Here a function could be called that analyzes the job advertisement and the process and optimizes it
                # Example:
                st.write("Optimization suggestions for the job advertisement:")
                st.write("- Use more action-oriented verbs.")
                st.write("- Emphasize the most important benefits more clearly.")
                st.write("Optimization suggestions for the recruitment process:")
                st.write("- Shorten the time until the first feedback to applicants.")
                st.write("- Implement a structured interview process.")
                time.sleep(2)  # Simulation of a longer processing time
                st.success("AI optimization completed!")
        except Exception as e:
            handle_error(e, "Error in AI optimization.")

    # PDF Export
    if st.button("PDF Export"):
        try:
            with st.spinner("Generating PDF..."):
                pdf = generate_pdf_report()
                st.download_button(
                    label="Download PDF",
                    data=pdf.output(dest="S").encode("latin-1"),
                    file_name="job_summary.pdf",
                    mime="application/pdf",
                )
        except Exception as e:
            handle_error(e, "Error generating PDF.")

    # Buttons for further actions
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Prepare Interview Questions"):
            try:
                data_for_prompt = prepare_data_for_prompt(st.session_state)
                prompt = generate_interview_questions_prompt(
                    data_for_prompt, st.session_state.job_details["job_title"]
                )
                with st.spinner("Generating interview questions..."):
                    generated_interview_questions = generate_text_with_ollama(prompt)

                st.session_state.generated_interview_questions = (
                    generated_interview_questions
                )
            except Exception as e:
                handle_api_error(e, "AI model")

    with col2:
        if st.button("Create Onboarding Checklist"):
            try:
                data_for_prompt = prepare_data_for_prompt(st.session_state)
                prompt = generate_onboarding_checklist_prompt(
                    data_for_prompt, st.session_state.job_details["job_title"]
                )

                with st.spinner("Generating onboarding checklist..."):
                    generated_onboarding_checklist = generate_text_with_ollama(prompt)

                st.session_state.generated_onboarding_checklist = (
                    generated_onboarding_checklist
                )
            except Exception as e:
                handle_api_error(e, "AI model")

    with col3:
        if st.button("Suggest Retention Strategies"):
            try:
                data_for_prompt = prepare_data_for_prompt(st.session_state)
                prompt = generate_retention_strategies_prompt(
                    data_for_prompt, st.session_state.job_details["job_title"]
                )
                with st.spinner("Generating employee retention strategies..."):
                    generated_retention_strategies = generate_text_with_ollama(prompt)

                st.session_state.generated_retention_strategies = (
                    generated_retention_strategies
                )
            except Exception as e:
                handle_api_error(e, "AI model")

    # Display the generated content in expanders
    if (
        "generated_interview_questions" in st.session_state
        and st.session_state.generated_interview_questions
    ):
        with st.expander("Generated Interview Questions", expanded=True):
            st.write(st.session_state.generated_interview_questions)
    if (
        "generated_onboarding_checklist" in st.session_state
        and st.session_state.generated_onboarding_checklist
    ):
        with st.expander("Generated Onboarding Checklist", expanded=True):
            st.write(st.session_state.generated_onboarding_checklist)
    if (
        "generated_retention_strategies" in st.session_state
        and st.session_state.generated_retention_strategies
    ):
        with st.expander("Generated Retention Strategies", expanded=True):
            st.write(st.session_state.generated_retention_strategies)

def generate_pdf_report():
    """Generates a PDF report from the collected data."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)

    # Define a function to add text with automatic font size adjustment
    def add_text_with_font_size_adjustment(text, max_width, font_size, style=''):
        """
        Adds a text block to a PDF and reduces the font size
        if the text exceeds the maximum width.
        """
        pdf.set_font("Arial", style, font_size)
        text_width = pdf.get_string_width(text)

        # Reduce the font size if the text is too wide
        while text_width > max_width and font_size > 8:
            font_size -= 1
            pdf.set_font("Arial", style, font_size)
            text_width = pdf.get_string_width(text)

        pdf.multi_cell(max_width, 10, text)

    # Add title
    pdf.cell(0, 10, "Job Summary", 0, 1, "C")
    pdf.set_font("Arial", "", 12)

    # Job Details
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Job Details", 0, 1)
    pdf.set_font("Arial", "", 12)
    for key, value in st.session_state.job_details.items():
        # Skip the section if the value is None
        if value is None:
            continue
        # Convert the value to a string before calling replace
        value_str = str(value)
        add_text_with_font_size_adjustment(f"{key.replace('_', ' ').capitalize()}: {value_str}", 190, 12)

    # Company Info
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Company Info", 0, 1)
    pdf.set_font("Arial", "", 12)
    for key, value in st.session_state.company_info.items():
        # Skip the section if the value is None
        if value is None:
            continue
        value_str = str(value)
        add_text_with_font_size_adjustment(f"{key.replace('_', ' ').capitalize()}: {value_str}", 190, 12)

    # Department Info (only the relevant keys)
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Department Info", 0, 1)
    pdf.set_font("Arial", "", 12)
    relevant_keys = [
        "department",
        "department_keywords",
        "department_size",
        "team_size",
        "reporting_line",
        "internal_contact",
        "budget_authority",
        "hiring_authority",
        "requisition_originator",
        "direct_supervisor",
        "contact_email_hiring",
        "contact_phone_hiring",
        "contact_email_requisition",
        "contact_phone_requisition",
    ]
    for key in relevant_keys:
        if key in st.session_state.job_details:
            value = st.session_state.job_details[key]
            # Skip the section if the value is None
            if value is None:
                continue
            value_str = str(value)
            add_text_with_font_size_adjustment(f"{key.replace('_', ' ').capitalize()}: {value_str}", 190, 12)

    # Role Info (only the relevant keys)
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Role Info", 0, 1)
    pdf.set_font("Arial", "", 12)
    relevant_keys = [
        "job_title",
        "start_date",
        "contract_type",
        "job_location",
        "onsite_percentage",
        "work_arrangement",
        "work_model",
        "travel_requirements",
        "priority",
        "training_budget",
        "salary_range",
        "vacancy_reason",
        "experience_level",
    ]
    for key in relevant_keys:
        if key in st.session_state.job_details:
            value = st.session_state.job_details[key]
            # Skip the section if the value is None
            if value is None:
                continue
            value_str = str(value)
            add_text_with_font_size_adjustment(f"{key.replace('_', ' ').capitalize()}: {value_str}", 190, 12)

    # Skills (only the relevant keys)
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Skills", 0, 1)
    pdf.set_font("Arial", "", 12)
    relevant_keys = [
        "required_skills",
        "experience_level_min_req",
        "experience_level_max_req",
        "technical_skills",
        "experience_level_min_tech",
        "experience_level_max_tech",
        "desired_certifications",
        "education_level",
        "soft_skills",
        "experience_level_min_soft",
        "experience_level_max_soft",
        "required_languages",
        "experience_level_min_lang",
        "experience_level_max_lang",
    ]
    for key in relevant_keys:
        if key in st.session_state.job_details:
            value = st.session_state.job_details[key]
            # Skip the section if the value is None
            if value is None:
                continue
            value_str = str(value)
            add_text_with_font_size_adjustment(f"{key.replace('_', ' ').capitalize()}: {value_str}", 190, 12)

    # Tasks
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Tasks", 0, 1)
    pdf.set_font("Arial", "", 12)
    for task, frequency in st.session_state.task_frequencies.items():
        add_text_with_font_size_adjustment(f"{task}: {frequency}", 190, 12)

    # Recruitment Process
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Recruitment Process", 0, 1)
    pdf.set_font("Arial", "", 12)
    for step in st.session_state.selected_recruitment_steps:
        add_text_with_font_size_adjustment(f"{step}", 190, 12)
        duration_key = f"duration_{step}"
        if duration_key in st.session_state.job_details:
            duration = st.session_state.job_details[duration_key]
            add_text_with_font_size_adjustment(f"  Duration: {duration} days", 190, 12)
        responsible_key = f"responsible_{step}"
        if responsible_key in st.session_state.job_details:
            responsible = st.session_state.job_details[responsible_key]
            add_text_with_font_size_adjustment(f"  Responsible: {responsible}", 190, 12)
    if "current_recruitment_process" in st.session_state.job_details:
        add_text_with_font_size_adjustment(f"Current Process: {st.session_state.job_details['current_recruitment_process']}", 190, 12)

    # Benefits
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Benefits", 0, 1)
    pdf.set_font("Arial", "", 12)
    for benefit in st.session_state.selected_benefits:
        add_text_with_font_size_adjustment(f"{benefit}", 190, 12)

    # Generated Job Ad
    if "generated_job_ad" in st.session_state and st.session_state.generated_job_ad:
        pdf.ln(10)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Generated Job Ad", 0, 1)
        pdf.set_font("Arial", "", 12)
        add_text_with_font_size_adjustment(st.session_state.generated_job_ad, 190, 12, style='')

    # Job Ad A/B Testing (falls vorhanden)
    if "generated_job_ad_a" in st.session_state and st.session_state.generated_job_ad_a:
        pdf.ln(10)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Generated Job Ad (Variant A)", 0, 1)
        pdf.set_font("Arial", "", 12)
        add_text_with_font_size_adjustment(st.session_state.generated_job_ad_a, 190, 12, style='')

    if "generated_job_ad_b" in st.session_state and st.session_state.generated_job_ad_b:
        pdf.ln(10)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Generated Job Ad (Variant B)", 0, 1)
        pdf.set_font("Arial", "", 12)
        add_text_with_font_size_adjustment(st.session_state.generated_job_ad_b, 190, 12, style='')

    return pdf

if __name__ == "__main__":
    main()