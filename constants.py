import streamlit as st
from config import DEV_MODE

# directories
DATA_ROOT = "./temp_data"
REPOS_DIR_NAME = "repos"
DB_DIR_NAME = "db"

# oauth2
BASE_URI = "http://localhost:8501" if DEV_MODE else "https://repo-amigo.streamlit.app"
CLIENT_ID = (
    st.secrets["GITHUB_CLIENT_ID_DEV"] if DEV_MODE else st.secrets["GITHUB_CLIENT_ID"]
)
CLIENT_SECRET = (
    st.secrets["GITHUB_CLIENT_SECRET_DEV"]
    if DEV_MODE
    else st.secrets["GITHUB_CLIENT_SECRET"]
)
REDIRECT_URI = f"{BASE_URI}/oauth-callback"
GITHUB_AUTHORIZATION_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"
