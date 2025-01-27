# ui_elements.py
import streamlit as st
import base64

def centered_title(title):
    """Displays a centered title."""
    st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)

def section_title(title):
    """Displays a section title."""
    st.markdown(f"<h2 style='color: #ff9f33;'>{title}</h2>", unsafe_allow_html=True)

def error_message(message):
    """Displays an error message."""
    st.error(message)

def success_message(message):
    """Displays a success message."""
    st.success(message)

def warning_message(message):
    """Displays a warning message."""
    st.warning(message)

def labeled_selectbox(label="selectbox", options=[], key="selectbox_input", index=0, help_text=""):
    """
    Displays a labeled select box.

    Args:
        label (str): The label of the select box.
        options (list): A list of options to display in the select box.
        key (str): The unique key for the select box.
        index (int, optional): The index of the default selected option. Defaults to 0.
        help_text (str, optional): A help text displayed below the select box. Defaults to "".

    Returns:
        str: The selected option.
    """
    with st.container():
        st.write(f"**{label}**")
        selectbox_input = st.selectbox(
            label, options=options, key=key, index=index, help=help_text, label_visibility="collapsed"
        )
        return selectbox_input

def labeled_number_input(label="Please enter number:", key="number_input", value=0, min_value=None, max_value=None, step=None, help_text=""):
    """
    Displays a labeled number input field.

    Args:
        label (str): The label of the input field.
        key (str): The unique key for the input field.
        value (int or float, optional): The default value of the input field. Defaults to 0.
        min_value (int or float, optional): The minimum value of the input field. Defaults to None.
        max_value (int or float, optional): The maximum value of the input field. Defaults to None.
        step (int or float, optional): The step value of the input field. Defaults to None.
        help_text (str, optional): A help text displayed below the input field. Defaults to "".

    Returns:
        int or float: The entered number.
    """
    with st.container():
        st.write(f"**{label}**")
        number_input = st.number_input(
            label,
            key=key,
            value=value,
            min_value=min_value,
            max_value=max_value,
            step=step,
            help=help_text,
            label_visibility="collapsed"
        )
        return number_input

def labeled_text_input(label="Please enter:", key="text_input", value="", placeholder="", help_text=""):
    """
    Displays a labeled text input field.

    Args:
        label (str): The label of the input field.
        key (str): The unique key for the input field.
        value (str, optional): The default value of the input field. Defaults to "".
        placeholder (str, optional): The placeholder text in the input field. Defaults to "".
        help_text (str, optional): A help text displayed below the input field. Defaults to "".

    Returns:
        str: The entered text.
    """
    with st.container():
        st.write(f"**{label}**")
        text_input = st.text_input(
            label, key=key, value=value, placeholder=placeholder, help=help_text, label_visibility="collapsed"
        )
        return text_input
    
def labeled_text_area(label="Please enter text", key="text_area_input", value="", placeholder="", height=None, help_text=""):
    """
    Displays a labeled text area field.

    Args:
        label (str): The label of the text area.
        key (str): The unique key for the text area.
        value (str, optional): The default value of the text area. Defaults to "".
        placeholder (str, optional): The placeholder text in the text area. Defaults to "".
        height (int, optional): The height of the text area in pixels. Defaults to None.
        help_text (str, optional): A help text displayed below the text area. Defaults to "".

    Returns:
        str: The entered text.
    """
    with st.container():
        st.write(f"**{label}**")
        text_area_input = st.text_area(
            label, key=key, value=value, placeholder=placeholder, height=height, help=help_text, label_visibility="collapsed"
        )
        return text_area_input

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def get_img_with_href(local_file, context_type="static"):
    """Generates a link allowing the user to download a local file."""
    binary_string = get_base64_of_bin_file(local_file)
    return binary_string

def labeled_multiselect(label="multiselect", options=[], key="multiselect_input", default=None, help_text=""):
    """
    Displays a labeled multiselect field.

    Args:
        label (str): The label of the multiselect field.
        options (list): A list of options to display in the multiselect field.
        key (str): The unique key for the multiselect field.
        default (list, optional): A list of default selected options. Defaults to None.
        help_text (str, optional): A help text displayed below the multiselect field. Defaults to "".

    Returns:
        list: The selected options.
    """
    # Check if there are already selections made by the user
    # Use the key to get the current value from session state
    if key in st.session_state and st.session_state[key]:
        default = st.session_state[key]
    elif default is None:
        default = []
    
    with st.container():
        st.write(f"**{label}**")
        multiselect_input = st.multiselect(
            label, options=options, key=key, default=default, help=help_text, label_visibility="collapsed"
        )
        return multiselect_input

def labeled_checkbox(label="checkbox", key="checkbox_input", value=False, help_text=""):
    """
    Displays a labeled checkbox.

    Args:
        label (str): The label of the checkbox.
        key (str): The unique key for the checkbox.
        value (bool, optional): The default state of the checkbox (checked or unchecked). Defaults to False.
        help_text (str, optional): A help text displayed below the checkbox. Defaults to "".

    Returns:
        bool: True if the checkbox is checked, False otherwise.
    """
    with st.container():
        checkbox_input = st.checkbox(label, key=key, value=value, help_text=help_text, label_visibility="collapsed")
        return checkbox_input

def labeled_date_input(label="labeled_date_input", key="date_input", value=None, help_text=""):
    """
    Displays a labeled date input field.

    Args:
        label (str): The label of the date input field.
        key (str): The unique key for the date input field.
        value (datetime.date, optional): The default value of the date input field. Defaults to None.
        help_text (str, optional): A help text displayed below the date input field. Defaults to "".

    Returns:
        datetime.date: The selected date.
    """
    with st.container():
        st.write(f"**{label}**")
        date_input = st.date_input(label, key=key, value=value, help=help_text, label_visibility="collapsed")
        return date_input

def labeled_slider(label="slider", min_value=0, max_value=100, key="slider_input", value=None, step=None, help_text=""):
    """
    Displays a labeled slider. Uses `st.slider` for desktop
    and `st.select_slider` for mobile devices to improve usability.

    Args:
        label (str): The label of the slider.
        min_value (int or float): The minimum value of the slider.
        max_value (int or float): The maximum value of the slider.
        key (str): The unique key for the slider.
        value (int or float, optional): The default value of the slider. Defaults to None.
        step (int or float, optional): The step value of the slider. Defaults to None.
        help_text (str, optional): A help text displayed below the slider. Defaults to "".

    Returns:
        int or float: The selected value of the slider.
    """
    with st.container():
        st.write(f"**{label}**")
        if st.session_state.get("is_mobile", False):
            # For mobile devices: use select_slider
            options = list(range(min_value, max_value + 1, step if step is not None else 1)) 
            value = value if value is not None else min_value
            slider_input = st.select_slider(
                label, options=options, key=key, value=value, help=help_text, label_visibility="collapsed"
            )
        else:
            # For desktop: use slider
            value = value if value is not None else min_value
            slider_input = st.slider(
                label,
                min_value=min_value,
                max_value=max_value,
                key=key,
                value=value,
                step=step,
                help=help_text,
                label_visibility="collapsed"
            )
        return slider_input

def labeled_radio(label="radio", options=[], key="radio_input", index=0, horizontal=False, help_text=""):
    """
    Displays labeled radio buttons.

    Args:
        label (str): The label of the radio buttons.
        options (list): A list of options to display in the radio buttons.
        key (str): The unique key for the radio buttons.
        index (int, optional): The index of the default selected option. Defaults to 0.
        horizontal (bool, optional): Whether to display the radio buttons horizontally. Defaults to False.
        help_text (str, optional): A help text displayed below the radio buttons. Defaults to "".

    Returns:
        str: The selected option.
    """
    with st.container():
        st.write(f"**{label}**")
        radio_input = st.radio(
            label,
            options=options,
            key=key,
            index=index,
            horizontal=horizontal,
            help=help_text,
            label_visibility="collapsed"
        )
        return radio_input