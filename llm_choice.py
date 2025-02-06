import streamlit as st

# Benutzerentscheidung: Lokales LLM oder OpenAI API
def llm_choice_ui():
    st.subheader("🔍 Wähle deine AI-Engine")
    
    llm_options = ["Lokales LLM", "OpenAI API"]
    selected_llm = st.radio("Wie soll die AI-Generierung erfolgen?", llm_options)

    # Speichern der Auswahl in `st.session_state`
    if selected_llm == "Lokales LLM":
        st.session_state["llm_mode"] = "local"
    else:
        st.session_state["llm_mode"] = "openai"

    st.success(f"✅ AI-Generierung erfolgt über: **{selected_llm}**")
