import streamlit as st
from text_to_speech import text_to_speech

st.set_page_config(page_title="Summary", page_icon="📝")

st.title("📝 Summary")

if st.session_state.get("summary"):
    summary = st.session_state.summary
    st.markdown(f'<p class="summary-text">{summary}</p>', unsafe_allow_html=True)

    if st.button("🔊 Listen to Summary"):
        text_to_speech(summary)
        audio_bytes = open("summary.mp3", "rb").read()
        st.audio(audio_bytes, format="audio/mp3")
else:
    st.warning("No summary available. Please upload a file and generate the summary on the 📚 Home page.")
