import streamlit as st
import os
import datetime

# Define chat storage folder
CHAT_FOLDER = 'code/'
os.makedirs(CHAT_FOLDER, exist_ok=True)
CHAT_FILE = os.path.join(CHAT_FOLDER, 'chat_history.txt')

# User authentication
USERNAME = "SUBHAJIT8167"
PASSWORD = "816785"

st.set_page_config(page_title="Live Group Chat", layout="wide")

st.title("💬 Live Group Chat")

# Login system
username_input = st.text_input("Enter Username")
password_input = st.text_input("Enter Password", type="password")
login_button = st.button("Login")

if login_button:
    if username_input == USERNAME and password_input == PASSWORD:
        st.session_state["logged_in"] = True
    else:
        st.error("Invalid username or password")

if "logged_in" in st.session_state and st.session_state["logged_in"]:
    st.success("✅ Logged in successfully!")
    
    # Chat input
    message = st.text_area("Type your message")
    send_button = st.button("Send")
    
    if send_button and message:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(CHAT_FILE, "a") as f:
            f.write(f"[{timestamp}] {USERNAME}: {message}\n")
        st.rerun()

    
    # Display chat history
    st.subheader("📜 Chat History")
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as f:
            chat_history = f.read()
            st.text_area("", chat_history, height=300, disabled=True)
else:
    st.warning("Please log in to access the chat.")
