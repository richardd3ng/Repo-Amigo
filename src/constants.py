from config import DEV_MODE

# directories
DATA_ROOT = "./temp_data"
REPOS_DIR_NAME = "repos"
DB_DIR_NAME = "db"

# oauth2
BASE_URI = "http://localhost:8501" if DEV_MODE else "https://repo-amigo.streamlit.app"
REDIRECT_URI = f"{BASE_URI}/github-code"
GITHUB_AUTHORIZATION_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"
