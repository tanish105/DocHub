import os
from PIL import Image
from account import MONGO_HOST, MONGO_URI, MONGO_USER
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from urllib.parse import quote_plus
import pymongo
from pymongo.server_api import ServerApi

load_dotenv()
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_USER = quote_plus(os.getenv("MONGO_USER"))
MONGO_PASS = quote_plus(os.getenv("MONGO_PASS"))
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}/?retryWrites=true&w=majority"

client = pymongo.MongoClient(MONGO_URI, server_api=ServerApi('1'))
database = client.get_database('dochub')
collection = database.get_collection('invoices')

def add_invoices(uploaded_file,text,response):
    if uploaded_file is not None:
        collection.insert_one({"image": uploaded_file.getvalue(),"query":text,"response":response})
        st.success("Invoice uploaded successfully")

def app():
    load_dotenv()
    genai.configure(api_key=os.getenv("GENAI_API_KEY"))

    # function to load gemini
    model = genai.GenerativeModel('gemini-1.5-flash')

    def get_gemini_response(input, image, prompt):
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

    # Initialize the streamlit app
    st.header("Invoice Extractor") 
    input = st.text_input("Enter the details you want from the invoice", key="input")
    uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])
    image = ""
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Invoice.', use_column_width=True)

    submit = st.button("Submit")

    input_prompt = """
    You are an expert in understanding invoices. We will upload an image of an invoice and you will have to answer questions based on
    the uploaded invoice.
    """

    # If submit is clicked
    if submit:
        image_data = input_image(uploaded_file)
        response = get_gemini_response(input, image_data, input_prompt)
        add_invoices(uploaded_file,input,response)
        st.subheader("The response is")
        st.write(response)

# Call the app function
if __name__ == "__main__":
    app()
