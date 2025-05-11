from pdf_reader import extract_text_from_pdf
from summarizer import summarize
from text_to_speech import speak_text

pdf_path =r"C:\Users\gargi\Desktop\Python\AI Study_assistant\Dataset for AI-Powered Digital Twin space and aerospace.txt"
text = extract_text_from_pdf(pdf_path)

print("\n--- Extracted Text (First 1000 characters) ---")
print(text[:5000])

summary = summarize(text)
print("\n--- Summary ---")
print(summary)
speak_text(summary)