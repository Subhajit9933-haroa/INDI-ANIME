import streamlit as st
from auth import login, register
from upload import upload_post
from timeline import display_timeline

def main():
    st.title("Twitter Clone")
    
    menu = ["Home", "Login", "Register", "Upload", "Timeline"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "Home":
        st.subheader("Welcome to the Twitter Clone!")
    
    elif choice == "Login":
        username, password = login()
        if username and password:
            st.success(f"Logged in as {username}")
    
    elif choice == "Register":
        username, password = register()
        if username and password:
            st.success(f"Registered as {username}")
    
    elif choice == "Upload":
        upload_post()
    
    elif choice == "Timeline":
        display_timeline()

if __name__ == "__main__":
    main()