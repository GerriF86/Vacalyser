import streamlit as st

def main():  # Stelle sicher, dass diese Funktion existiert
    st.markdown('<div class="about-section">', unsafe_allow_html=True)
st.markdown('<p class="about-title">About RecruitSmarts</p>', unsafe_allow_html=True)
st.markdown(
            """
            <p class="about-text">
            <b>RecruitSmarts</b> is a cutting-edge Streamlit web application designed to eliminate information loss in the crucial first steps of the hiring process. 
            We understand that a successful hire starts with a deep understanding of the role, and that's where our AI-powered solution comes in.
            </p>
            <p class="about-text">
            <b>Here's how we do it:</b>
            <ul>
                <li><b>Dynamic Questioning:</b> Our intelligent system guides hiring managers through a series of tailored questions, probing beyond the surface to uncover the nuances of each role.</li>
                <li><b>Local AI with Ollama 3.2 3B:</b> We leverage the power of a state-of-the-art, locally-run language model. This means your sensitive data never leaves your computer, ensuring maximum privacy and security.</li>
                <li><b>Actionable Insights:</b> RecruitSmarts transforms the collected data into a goldmine of information. Generate targeted job ads, pinpoint the best recruitment channels, and create comprehensive interview prep sheets – all from one centralized hub.</li>
                <li><b>Built for Efficiency:</b> No more tedious forms or lost emails. Our streamlined process saves you time and resources, allowing you to focus on what matters most – finding the perfect candidate.</li>
            </ul>
            </p>
            <p class="about-text">
            <b>Why choose local AI?</b>
            <ul>
                <li><b>Data Privacy:</b> Your vacancy information is highly sensitive. Running locally guarantees that it stays within your control.</li>
                <li><b>Offline Access:</b> No internet? No problem. Document vacancies anytime, anywhere.</li>
                <li><b>Cost-Effective:</b> Avoid expensive cloud API calls. Our solution is designed to be budget-friendly.</li>
                <li><b>Lightning-Fast:</b> Local processing means instant responses and a smooth, seamless user experience.</li>
            </ul>
            </p>
            <p class="about-text">
            <b>RecruitSmarts</b> is more than just a data collection tool. It's your strategic partner in building a stronger, more successful workforce. We empower you to attract, identify, and hire top talent with confidence, setting the stage for long-term employee retention and organizational growth.
            </p>
            """,
            unsafe_allow_html=True,
        )
st.markdown('</div>', unsafe_allow_html=True)
if __name__ == "__main__":
    main()