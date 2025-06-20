# app.py
import streamlit as st
import json
import os
from datetime import datetime
from hashlib import sha256

USERS_FILE = "users.json"
POSTS_FILE = "posts.json"
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

def load_json(file, default):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump(default, f)
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def signup(username, password):
    users = load_json(USERS_FILE, [])
    if any(u["username"] == username for u in users):
        return False, "Username already exists."
    users.append({"username": username, "password": hash_password(password)})
    save_json(USERS_FILE, users)
    return True, "Signup successful!"

def login(username, password):
    users = load_json(USERS_FILE, [])
    for u in users:
        if u["username"] == username and u["password"] == hash_password(password):
            return True
    return False

def save_post(username, text, image_path=None):
    posts = load_json(POSTS_FILE, [])
    posts.append({
        "username": username,
        "text": text,
        "image": image_path,
        "time": datetime.now().isoformat()
    })
    save_json(POSTS_FILE, posts)

def get_posts():
    return reversed(load_json(POSTS_FILE, []))

st.set_page_config(page_title="Akta Twitter Clone", layout="centered")
st.title("Akta Twitter Clone")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

menu = st.sidebar.selectbox("Menu", ["Login", "Signup"] if not st.session_state.logged_in else ["Timeline", "Logout"])

if not st.session_state.logged_in:
    if menu == "Signup":
        st.subheader("Sign Up")
        su_user = st.text_input("Username", key="su_user")
        su_pass = st.text_input("Password", type="password", key="su_pass")
        if st.button("Sign Up"):
            ok, msg = signup(su_user, su_pass)
            st.info(msg)
    elif menu == "Login":
        st.subheader("Login")
        li_user = st.text_input("Username", key="li_user")
        li_pass = st.text_input("Password", type="password", key="li_pass")
        if st.button("Login"):
            if login(li_user, li_pass):
                st.session_state.logged_in = True
                st.session_state.username = li_user
                st.success("Logged in!")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials.")
else:
    if menu == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("Logged out!")
        st.experimental_rerun()
    elif menu == "Timeline":
        st.subheader(f"Welcome, {st.session_state.username}!")
        st.markdown("### Create a Post")
        post_text = st.text_area("What's happening?")
        post_image = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])
        if st.button("Post"):
            img_path = None
            if post_image:
                img_path = os.path.join(UPLOAD_DIR, f"{datetime.now().timestamp()}_{post_image.name}")
                with open(img_path, "wb") as f:
                    f.write(post_image.read())
            save_post(st.session_state.username, post_text, img_path)
            st.success("Posted!")
        st.markdown("---")
        st.markdown("### Timeline")
        for post in get_posts():
            st.write(f"**{post['username']}** at {post['time'][:19]}")
            st.write(post["text"])
            if post["image"]:
                st.image(post["image"], width=300)
            st.markdown("---")