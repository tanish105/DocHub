import streamlit as st

def app():
    
    st.title('Welcome to :violet[DocHub] 📃')
     
    choice = st.selectbox("Login/SignUp", ["Login", "SignUp"])
    if choice == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        st.button("Login")
    else:
        email = st.text_input("Email")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        st.button("Sign Up")