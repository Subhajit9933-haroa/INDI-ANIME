# Twitter Clone Streamlit

This project is a Twitter-like web application built using Streamlit. It allows users to register, log in, and post text and photos. The application features a timeline where users can view posts made by others.

## Features

- User registration and login
- Upload text and photo posts
- View a timeline of posts
- Data stored in JSON format

## Project Structure

```
twitter_clone_streamlit
├── src
│   ├── app.py          # Main entry point of the application
│   ├── auth.py         # User authentication functions
│   ├── upload.py       # Functions for uploading posts
│   ├── timeline.py     # Displays the timeline of posts
│   ├── utils.py        # Utility functions
│   └── data
│       ├── users.json  # Stores user data
│       └── posts.json  # Stores posts data
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd twitter_clone_streamlit
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   streamlit run src/app.py
   ```

2. Follow the on-screen instructions to register or log in.

3. Once logged in, you can upload text and photo posts and view the timeline.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License.