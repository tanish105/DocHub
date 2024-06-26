from urllib.parse import quote_plus
import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
import PyPDF2 as pdf
import pymongo
from pymongo.server_api import ServerApi

load_dotenv()
MONGO_USER = quote_plus(os.getenv("MONGO_USER"))
MONGO_PASS = quote_plus(os.getenv("MONGO_PASS"))
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}/?retryWrites=true&w=majority"

client = pymongo.MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client.get_database('dochub')
resume_collection = db.get_collection('resume')

def add_resume(uploaded_file, text, response):
    if uploaded_file is not None:
        resume_collection.insert_one({"resume": uploaded_file.getvalue(), "query": text, "response": response})
        st.success("Resume stored successfully")

def app():
    # Load environment variables
    load_dotenv()

    # Configure Generative AI
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # Function to get the response from the model
    def get_response(input):
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([input])
        return response.text

    # Function to get the resume text from a PDF
    def pdf_text(uploaded_file):
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    # Input prompt template
    input_prompt = """
    Hey Act Like a skilled or very experienced ATS(Application Tracking System)
    with a deep understanding of tech field, software engineering, data science, data analyst,
    and big data engineer. Your task is to evaluate the resume based on the given job description.
    You must consider the job market is very competitive and you should provide 
    best assistance for improving the resumes. Assign the percentage matching based 
    on the JD and
    the missing keywords with high accuracy.
    resume: {resume_text}
    description: {jd}

    I want the response in one single string having the structure
    {{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}}
    """

    # Streamlit app
    st.title("Resume Analyzer")
    st.write("Upload a resume and a job description to get the summary!")
    jd = st.text_input("Enter the job description")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf"])

    submit = st.button("Submit")

    if submit:
        if uploaded_file is not None:
            resume_text = pdf_text(uploaded_file)
            prompt = input_prompt.format(resume_text=resume_text, jd=jd)
            response = get_response(prompt)
            add_resume(uploaded_file, jd, response)
            st.subheader("Analysis Result")
            st.code(response, language='json')
        else:
            st.warning("Please upload a PDF file.")

# Call the app function
if __name__ == "__main__":
    app()
