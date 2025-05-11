# text_to_speech.py
import pyttsx3

def text_to_speech(text, filename="summary.mp3"):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.save_to_file(text, filename)
    engine.runAndWait()
