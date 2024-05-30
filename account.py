from json import load
import streamlit as st
import pymongo
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()
MONGO_USER = quote_plus(os.getenv("MONGO_USER"))
MONGO_PASS = quote_plus(os.getenv("MONGO_PASS"))
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}/?retryWrites=true&w=majority"

client = pymongo.MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client.get_database('dochub')
users_collection = db.get_collection('users')

def add_user(email, username, password):
    user_data = {
        'email':email,
        'username':username,
        'password':password
    }
    users_collection.insert_one(user_data)

def find_user(username, password):
    user_data = users_collection.find_one({'username':username, 'password':password})
    return user_data

def app():
    
    st.title('Welcome to :violet[DocHub] 📃')
     
    choice = st.selectbox("Login/SignUp", ["Login", "SignUp"])
    if choice == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user_data = find_user(username, password)
            if user_data:
                st.success("You have successfully logged in!")
                st.balloons()
            else:
                st.warning("Invalid Username/Password")
    else:
        email = st.text_input("Email")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Sign Up"):
            add_user(email, username, password)
            st.success("You have successfully signed up!")