import os
from PIL import Image
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

def app():
    st.title("New Page")
    st.header("Invoice Extractor 2")

    if st.button("Back to Main Page"):
        st.session_state['navigate'] = None
        st.experimental_rerun()

# Call the app function
if __name__ == "__main__":
    app()
