from urllib import response
from click import File
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GENAI_API_KEY"))

# function to load gemini
model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input,image,prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

#initialize the streamlit app
st.set_page_config(page_title="DocHub", page_icon="🌌", layout="wide")
st.header("Invoice Extractor")
input = st.text_input("Enter the details you want from the invoice",key = "input")
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Invoice.', use_column_width=True)

submit = st.button("submit")

input_prompt="""
You are an expert in understanding invoices. We will upload an image of an invoice and you will have to answer questions based on
the uploaded invoice.
"""

#if submit is clicked
if submit:
    image_data = input_image(uploaded_file)
    response = get_gemini_response(input,image_data,input)
    st.subheader("The response is")
    st.write(response)