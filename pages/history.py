import streamlit as st
import random

st.set_page_config(page_title="History", page_icon="📜")

st.title("📜 History of Summarized Files")

if st.session_state.get("history"):
    for file_name, summary in st.session_state.history:
        emoji = random.choice(["📄", "📝", "📚", "🔍"])
        st.markdown(f"### {emoji} File: {file_name}")
        st.markdown(f'<p class="summary-text">{summary}</p>', unsafe_allow_html=True)
        st.markdown("---")
else:
    st.info("No summary history found.")
