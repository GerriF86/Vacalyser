import streamlit as st

# UI für mehrspaltige Darstellung mit Karten
def column_layout_ui(section_title, left_content, right_content):
    st.subheader(section_title)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"### {left_content}")

    with col2:
        st.markdown(
            f'<div style="padding: 20px; background-color: #F3F4F6; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">'
            f'<p style="font-weight: bold; text-align: center;">{right_content}</p>'
            "</div>",
            unsafe_allow_html=True,
        )
