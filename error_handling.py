# error_handling.py
import streamlit as st
import logging
import config

# Configure logging
logging.basicConfig(
    level=config.LOGGING_CONFIG["level"],
    format=config.LOGGING_CONFIG["format"],
    filename=config.LOGGING_CONFIG["filename"],
)

def handle_error(e, message="An unknown error has occurred."):
    """
    Handles errors, displays an error message, and logs the error.

    Args:
        e (Exception): The exception that occurred.
        message (str): The error message to display.
    """
    logging.exception(f"Error: {e}")
    st.error(message + f" Details: {e}")

def handle_api_error(e, api_name):
    """
    Handles errors for API requests.
    """
    logging.exception(f"Error with {api_name} API request: {e}")
    st.error(
        f"An error occurred while communicating with {api_name}. Please try again later or check your API settings."
    )