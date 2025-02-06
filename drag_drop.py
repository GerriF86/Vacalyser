import streamlit as st

# UI für Drag & Drop
def drag_drop_ui(key, title):
    st.subheader(title)

    if key not in st.session_state:
        st.session_state[key] = []

    new_item = st.text_input(f"Neues Element hinzufügen ({title})")
    if st.button(f"➕ Hinzufügen zu {title}") and new_item:
        st.session_state[key].append(new_item)
        st.rerun()

    # Drag & Drop-Reihenfolge bearbeiten
    if st.session_state[key]:
        reordered_list = st.experimental_data_editor(st.session_state[key], num_rows="dynamic")
        st.session_state[key] = reordered_list
