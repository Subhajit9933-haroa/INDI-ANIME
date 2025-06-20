from streamlit import st
import json

def load_posts():
    with open('src/data/posts.json', 'r') as file:
        posts = json.load(file)
    return posts

def display_timeline():
    posts = load_posts()
    for post in posts:
        st.subheader(post['username'])
        st.write(post['content'])
        if 'image_url' in post:
            st.image(post['image_url'])
        st.write("---")

def main():
    st.title("Timeline")
    display_timeline()

if __name__ == "__main__":
    main()