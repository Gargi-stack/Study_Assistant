import streamlit as st
from pdf_reader import extract_text_from_pdf
from summarizer import summarize
from text_to_speech import text_to_speech
from docx import Document
from streamlit_lottie import st_lottie
import requests
import time

# Initialize session state
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'file' not in st.session_state:
    st.session_state.file = None
if 'history' not in st.session_state:
    st.session_state.history = []
if 'view_history' not in st.session_state:
    st.session_state.view_history = False

# Load Lottie animation
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_book = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_kkflmtur.json")
lottie_transition = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_usmfx6bp.json")

# Add Custom Styling with transition animations
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
        scroll-behavior: smooth;
    }

    body {
        background-color: #f5f5dc;
    }
    .stApp {
        background-color: #f5f5dc;
        color: #2d1e10;
    }
    label, .css-145kmo2 {
        color: #2d1e10 !important;
        font-weight: 600;
    }
    .stButton>button {
        background-color: #800000;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #a52a2a;
        color: white;
    }
    .stTextInput>div>div>input, .stFileUploader, .stSlider > div {
        background-color: #fff8dc;
        color: #2d1e10;
        padding: 10px;
        border-radius: 10px;
    }
    h1, h2, h3, h4, h5, h6 {
        text-align: center;
        color: #2d1e10;
    }
    .summary-text {
        color: #2d1e10;
        font-size: 16px;
        line-height: 1.6;
        animation: fadein 1s;
    }
    .history-entry {
        background-color: #fff8dc;
        padding: 10px;
        margin: 10px 0;
        border-left: 4px solid #800000;
        border-radius: 6px;
        transition: transform 0.3s ease-in-out;
    }
    .history-entry:hover {
        transform: scale(1.01);
    }
    @keyframes fadein {
        from { opacity: 0; }
        to   { opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)

# Lottie Animation Heading
st_lottie(lottie_book, height=150, key="header")

# App Heading
st.title("📚 AI Study Assistant")
st.markdown("## ✨ Summarize Text from PDFs, Word Documents, or Text Files")
st.markdown("Upload your file and get the summarized content here!")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Summary", "History"])

# Upload file
uploaded_file = st.file_uploader("📤 Upload a file (PDF, Word, or Text)", type=["pdf", "txt", "docx"])

def extract_text_from_word(docx_file):
    doc = Document(docx_file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

if page == "Home":
    # Home page content
    if uploaded_file:
        st.session_state.file = uploaded_file
        st.write("✅ File Uploaded: ", uploaded_file.name)

        # Summary length selection
        st.markdown("### ✂️ Choose Summary Length")
        length_option = st.select_slider(
        "Select the summary length",
        options=["Short", "Medium", "Long"],
        value="Medium"
     )

        if st.button("📝 Summarize Text"):
            with st.spinner("Generating summary..."):
                st_lottie(lottie_transition, height=120, key="load")
                time.sleep(1.5)

            if uploaded_file.type == "application/pdf":
                text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "text/plain":
                text = uploaded_file.getvalue().decode("utf-8")
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                text = extract_text_from_word(uploaded_file)

            summary = summarize(text, length=length_option.lower())
            st.session_state.summary = summary
            st.session_state.history.append((uploaded_file.name, summary))

    if st.session_state.summary:
        st.subheader("📄 Summary:")
        st.markdown(f'<p class="summary-text">{st.session_state.summary}</p>', unsafe_allow_html=True)

        if st.button("🔊 Listen to Summary"):
            text_to_speech(st.session_state.summary)
            audio_bytes = open("summary.mp3", "rb").read()
            st.audio(audio_bytes, format="audio/mp3")

elif page == "Summary":
    # Summary page content
    if st.session_state.get("summary"):
        summary = st.session_state.summary
        st.markdown(f'<p class="summary-text">{summary}</p>', unsafe_allow_html=True)

        if st.button("🔊 Listen to Summary"):
            text_to_speech(summary)
            audio_bytes = open("summary.mp3", "rb").read()
            st.audio(audio_bytes, format="audio/mp3")
    else:
        st.warning("No summary available. Please upload a file and generate the summary on the 📚 Home page.")

elif page == "History":
    # History page content
    if st.session_state.get("history"):
        for file_name, summary in st.session_state.history:
            st.markdown(f"### 📄 File: {file_name}")
            st.markdown(f'<p class="summary-text">{summary}</p>', unsafe_allow_html=True)
            st.markdown("---")
    else:
        st.info("No summary history found.")
