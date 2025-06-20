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
        "time": datetime.now().isoformat(),
        "comments": []
    })
    save_json(POSTS_FILE, posts)

def get_posts():
    return list(reversed(load_json(POSTS_FILE, [])))

def add_comment(post_index, commenter, comment_text):
    posts = load_json(POSTS_FILE, [])
    if 0 <= post_index < len(posts):
        if "comments" not in posts[post_index]:
            posts[post_index]["comments"] = []
        posts[post_index]["comments"].append({
            "commenter": commenter,
            "comment": comment_text,
            "time": datetime.now().isoformat()
        })
        save_json(POSTS_FILE, posts)

st.set_page_config(page_title="Akta Twitter Clone", layout="centered")
st.title("Akta Twitter Clone")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    menu = st.sidebar.selectbox("Menu", ["Login", "Signup"])
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
                st.success("Logged in! Please select 'Timeline' from the sidebar.")
            else:
                st.error("Invalid credentials.")
else:
    menu = st.sidebar.selectbox("Menu", ["Timeline", "Logout"])
    if menu == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("Logged out! Please select 'Login' from the sidebar.")
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
            st.success("Posted! Scroll down to see your post.")
        st.markdown("---")
        st.markdown("### Timeline")
        posts = get_posts()
        for idx, post in enumerate(posts):
            st.write(f"**{post['username']}** at {post['time'][:19]}")
            st.write(post["text"])
            if post["image"]:
                st.image(post["image"], width=300)
            # Show comments
            st.markdown("**Comments:**")
            comments = post.get("comments", [])
            if comments:
                for c in comments:
                    st.write(f"- {c['commenter']} ({c['time'][:19]}): {c['comment']}")
            else:
                st.write("_No comments yet._")
            # Add comment form
            with st.form(f"comment_form_{idx}"):
                comment_text = st.text_input("Add a comment:", key=f"comment_{idx}")
                submit_comment = st.form_submit_button("Comment")
                if submit_comment and comment_text.strip():
                    # posts is reversed, so original index is len(posts)-1-idx
                    add_comment(len(posts)-1-idx, st.session_state.username, comment_text.strip())
                    st.success("Comment added! Please scroll or refresh to see it.")
            st.markdown("---")
