import streamlit as st
import os
import json
import time
from PIL import Image

USERS_FILE = 'users.txt'
TWEETS_FILE = 'tweets.txt'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if ':' in line:
                    u, p = line.strip().split(':', 1)
                    users[u] = p
    return users

def save_user(username, password):
    with open(USERS_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{username}:{password}\n")

def load_tweets():
    if os.path.exists(TWEETS_FILE):
        with open(TWEETS_FILE, 'r', encoding='utf-8') as f:
            try:
                tweets = json.load(f)
                for t in tweets:
                    if 'id' not in t or not isinstance(t['id'], int):
                        t['id'] = int(time.time() * 1000) + hash(t['user'] + t['text'])
                    if 'comments' not in t or not isinstance(t['comments'], list):
                        t['comments'] = []
                return tweets
            except Exception:
                return []
    return []

def save_tweets(tweets):
    with open(TWEETS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tweets, f, ensure_ascii=False)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def save_image(uploaded_file, username, tweet_count):
    filename = f"{username}_{tweet_count}_{uploaded_file.name}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    # Validate image
    try:
        img = Image.open(filepath)
        img.verify()
        return filename
    except Exception:
        os.remove(filepath)
        return None

def rerun():
    # Compatible rerun for all Streamlit versions
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        st.rerun()

# Session state for login
if 'username' not in st.session_state:
    st.session_state['username'] = None

st.set_page_config(page_title="Knolage Sheare", page_icon="💡")
st.markdown("""
    <h1 style='color:#0d6efd;font-family:Segoe UI,sans-serif;'>Knolage Sheare</h1>
    """, unsafe_allow_html=True)

# Sidebar: Login/Register/Logout
users = load_users()
if st.session_state['username']:
    st.sidebar.success(f"Logged in as @{st.session_state['username']}")
    if st.sidebar.button("Logout"):
        st.session_state['username'] = None
        rerun()
else:
    tab1, tab2 = st.sidebar.tabs(["Login", "Register"])
    with tab1:
        login_user = st.text_input("Username", key="login_user")
        login_pass = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if login_user in users and users[login_user] == login_pass:
                st.session_state['username'] = login_user
                st.success("Login successful!")
                rerun()
            else:
                st.error("Invalid credentials")
    with tab2:
        reg_user = st.text_input("New Username", key="reg_user")
        reg_pass = st.text_input("New Password", type="password", key="reg_pass")
        if st.button("Register"):
            if reg_user in users:
                st.error("Username already exists")
            elif not reg_user or not reg_pass:
                st.error("Username and password required")
            else:
                save_user(reg_user, reg_pass)
                st.session_state['username'] = reg_user
                st.success("Registration successful!")
                rerun()

# Main: Post form
tweets = load_tweets()
if st.session_state['username']:
    with st.form("post_form", clear_on_submit=True):
        tweet_text = st.text_input("What's happening?", max_chars=280)
        tweet_img = st.file_uploader("Upload image", type=['png', 'jpg', 'jpeg', 'gif'])
        submitted = st.form_submit_button("Post")
        if submitted and tweet_text:
            photo_filename = None
            if tweet_img and allowed_file(tweet_img.name):
                photo_filename = save_image(tweet_img, st.session_state['username'], len(tweets))
            tweet_id = int(time.time() * 1000)
            tweets.append({
                'id': tweet_id,
                'user': st.session_state['username'],
                'text': tweet_text,
                'photo': photo_filename,
                'comments': []
            })
            save_tweets(tweets)
            rerun()

st.markdown("## Timeline")
for t in reversed(tweets):
    st.markdown(f"<div style='background:#23272b;padding:1em;border-radius:8px;margin-bottom:1em;'>", unsafe_allow_html=True)
    st.markdown(f"<b style='color:#0d6efd;'>@{t['user']}</b>: {t['text']}", unsafe_allow_html=True)
    if t.get('photo'):
        img_path = os.path.join(UPLOAD_FOLDER, t['photo'])
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
    st.markdown("<b>Comments:</b>", unsafe_allow_html=True)
    if t.get('comments'):
        for c in t['comments']:
            st.markdown(f"<div style='background:#1a1e22;padding:0.5em 1em;border-radius:6px;margin-bottom:0.5em;'><span style='color:#6ea8fe;font-weight:bold;'>@{c['user']}</span>: {c['text']}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<span style='color:#888;'>No comments yet.</span>", unsafe_allow_html=True)
    # Comment form
    if st.session_state['username']:
        with st.form(f"comment_form_{t['id']}"):
            comment_text = st.text_input("Add a comment...", max_chars=200, key=f"comment_{t['id']}")
            comment_submit = st.form_submit_button("Comment")
            if comment_submit and comment_text:
                for tw in tweets:
                    if tw['id'] == t['id']:
                        if not tw.get('comments'):
                            tw['comments'] = []
                        tw['comments'].append({'user': st.session_state['username'], 'text': comment_text})
                        save_tweets(tweets)
                        rerun()
    st.markdown("</div>", unsafe_allow_html=True)
