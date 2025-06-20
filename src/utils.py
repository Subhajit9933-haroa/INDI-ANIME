def read_json_file(file_path):
    import json
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def write_json_file(file_path, data):
    import json
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def validate_username(username):
    return isinstance(username, str) and len(username) > 0

def validate_password(password):
    return isinstance(password, str) and len(password) >= 6

def generate_post_id(posts):
    return len(posts) + 1 if posts else 1