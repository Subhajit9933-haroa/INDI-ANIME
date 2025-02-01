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

# Show login page first
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.title("💬 Live Group Chat - Login")

    # Login form
    with st.form(key='login_form'):
        username_input = st.text_input("Enter Username")
        password_input = st.text_input("Enter Password", type="password")
        login_button = st.form_submit_button("Login")
        
        if login_button:
            if username_input == USERNAME and password_input == PASSWORD:
                st.session_state['logged_in'] = True
                st.success("✅ Logged in successfully!")
            else:
                st.error("Invalid username or password")

else:
    st.title("💬 Live Group Chat")
    
    # Chat input and display
    st.subheader("📜 Chat History")
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as f:
            chat_history = f.read()
            # Display chat history in a disabled text area
            st.text_area("Chat History", chat_history, height=300, disabled=True)

    # Message input area (send box at the bottom)
    message = st.text_area("Type your message", min_rows=5)  # Use min_rows to control the height of the input box
    send_button = st.button("Send")
    
    if send_button and message:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(CHAT_FILE, "a") as f:
            f.write(f"[{timestamp}] {USERNAME}: {message}\n")
        st.experimental_rerun()
