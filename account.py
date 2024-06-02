from json import load

from requests import session
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
    st.session_state['username'] = user_data['username']
    st.session_state['email'] = user_data['email']
    st.session_state['logged_in'] = True
    return user_data

def app():
    #managing session state
    if 'username' not in st.session_state:
        st.session_state['username'] = ''
    if 'email' not in st.session_state:
        st.session_state['email'] = ''
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    st.title('Welcome to :violet[DocHub] 📃')
    if st.session_state['logged_in']:
        st.text(f"Logged in as {st.session_state['username']}")
        st.text(f"Email: {st.session_state['email']}")
        if st.button("Sign Out"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ''
            st.session_state['email'] = ''
            st.success("You have successfully logged out.")
    else:
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