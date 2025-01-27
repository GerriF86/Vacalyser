# data_processing.py
import re
import config
from email_validator import validate_email, EmailNotValidError

def validate_email_address(email):
    """Validates an email address."""
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def validate_phone_number(phone):
    """Validates a phone number (basic example)."""
    return re.match(r"^\+?[\d\s]+$", phone) is not None

def validate_website(url):
    """Validates a website URL."""
    return re.match(config.URL_PATTERN, url) is not None

def validate_text_length(text, max_length):
    """Validates the length of a text."""
    return len(text) <= max_length

def validate_salary_range(salary_range):
    """Validates a salary range."""
    try:
        lower, upper = map(int, salary_range.replace("k", "").split("-"))
        return lower < upper and lower >= 0
    except ValueError:
        return False

def prepare_data_for_prompt(session_state):
    """Prepares the data from the session state for prompt generation."""
    data = ""
    for key, value in session_state.items():
        if key in [
            "generated_job_ad",
            "generated_job_ad_a",
            "generated_job_ad_b",
            "generated_interview_questions",
            "generated_onboarding_checklist",
            "generated_retention_strategies",
            "current_page",
            "is_mobile",
            "username",
            "pdf_extracted_data",
            "last_updated",
            "job_category",
            "rag_chain"
        ]:
            continue

        if isinstance(value, dict):
            data += f"{key.replace('_', ' ').capitalize()}:\n"
            for subkey, subvalue in value.items():
                if subkey == "company_culture":
                    if subvalue:
                        data += (
                            f"  {subkey.replace('_', ' ').capitalize()}: {', '.join(subvalue)}\n"
                        )
                    else:
                        data += f"  {subkey.replace('_', ' ').capitalize()}: No entry\n"
                elif subkey == "selected_benefits":
                    if subvalue:
                        data += (
                            f"  {subkey.replace('_', ' ').capitalize()}: {', '.join(subvalue)}\n"
                        )
                    else:
                        data += f"  {subkey.replace('_', ' ').capitalize()}: No entry\n"
                elif subkey == "job_details":
                    for subsubkey, subsubvalue in subvalue.items():
                        data += (
                            f"   {subsubkey.replace('_', ' ').capitalize()}: {subsubvalue}\n"
                        )
                elif subkey == "company_info":
                    for subsubkey, subsubvalue in subvalue.items():
                        data += (
                            f"   {subsubkey.replace('_', ' ').capitalize()}: {subsubvalue}\n"
                        )
                elif isinstance(subvalue, list):
                    if subvalue:
                        data += (
                            f"  {subkey.replace('_', ' ').capitalize()}: {', '.join(subvalue)}\n"
                        )
                    else:
                        data += f"  {subkey.replace('_', ' ').capitalize()}: No entry\n"
                elif isinstance(subvalue, str):
                    if subvalue:
                        data += f"  {subkey.replace('_', ' ').capitalize()}: {subvalue}\n"
                    else:
                        data += f"  {subkey.replace('_', ' ').capitalize()}: No entry\n"
                elif isinstance(subvalue, int):
                    data += f"  {subkey.replace('_', ' ').capitalize()}: {subvalue}\n"
                else:
                    data += f"  {subkey.replace('_', ' ').capitalize()}: {subvalue}\n"
        elif isinstance(value, list):
            if value:
                data += f"{key.replace('_', ' ').capitalize()}: {', '.join(value)}\n"
            else:
                data += f"{key.replace('_', ' ').capitalize()}: No entry\n"
        elif isinstance(value, str):
            if value:
                data += f"{key.replace('_', ' ').capitalize()}: {value}\n"
            else:
                data += f"{key.replace('_', ' ').capitalize()}: No entry\n"
        elif isinstance(value, int):
            data += f"{key.replace('_', ' ').capitalize()}: {value}\n"
        elif isinstance(value, type(None)):
            data += f"{key.replace('_', ' ').capitalize()}: No entry\n"
        else:
            data += f"{key.replace('_', ' ').capitalize()}: {value}\n"

    return data