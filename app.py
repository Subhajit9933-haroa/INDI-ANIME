import streamlit as st
import os

# Define upload folder
UPLOAD_FOLDER = 'code/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Page Configuration
st.set_page_config(page_title="Video Streaming Platform", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stTextInput, .stFileUploader, .stButton {
        border-radius: 10px;
    }
    .stVideo {
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📺 Video Streaming Platform")
st.markdown("### Upload and Watch Videos Seamlessly!")

# File uploader with columns
col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("Upload a Video")
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov", "mkv"], key="uploader")
    title = st.text_input("Enter Video Title", key="title")
    if uploaded_file and title:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success(f"🎉 Uploaded: {title} ({uploaded_file.name})")

with col2:
    st.image("https://source.unsplash.com/600x300/?video,streaming", use_column_width=True)

# Display uploaded videos
st.subheader("📹 Available Videos")
video_list = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith((".mp4", ".avi", ".mov", ".mkv"))]

if video_list:
    for video in video_list:
        with st.container():
            st.markdown(f"**🎬 {video}**")
            st.video(os.path.join(UPLOAD_FOLDER, video))
else:
    st.info("No videos uploaded yet. Upload a video to start streaming!")
