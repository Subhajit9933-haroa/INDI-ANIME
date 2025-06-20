def upload_post(text, photo):
    import json
    import os

    posts_file = 'src/data/posts.json'

    # Load existing posts
    if os.path.exists(posts_file):
        with open(posts_file, 'r') as f:
            posts = json.load(f)
    else:
        posts = []

    # Create a new post entry
    new_post = {
        'text': text,
        'photo': photo,
    }

    # Append the new post to the list
    posts.append(new_post)

    # Save the updated posts back to the file
    with open(posts_file, 'w') as f:
        json.dump(posts, f)

def handle_file_upload(uploaded_file):
    import os

    if uploaded_file is not None:
        # Save the uploaded file to a designated folder
        file_path = os.path.join('src/data/uploads', uploaded_file.name)
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    return None