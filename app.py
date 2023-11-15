import git
import os
import shutil
import subprocess
import openai
import uuid
import hashlib
import tempfile
from collections import defaultdict
from urllib.parse import urlparse
import streamlit as st


st.title('Repo Amigo')

if github_url := st.text_input('GitHub Link to public repo:'):
    temp_dir = tempfile.TemporaryDirectory()
    try:
        st.write(temp_dir.name)
        repo_name = urlparse(github_url).path.split("/")[-1]
        repo_path = os.path.join(temp_dir.name, repo_name)
        st.write(repo_path)
        git.Repo.clone_from(github_url, repo_path)
    except Exception as e:
        st.error(f'Invalid GitHub URL: {e}')
    finally:
        temp_dir.cleanup()

# DB_PATH = os.path.join('./', f'db_{REPO_NAME}')

# # validate user API key
# with st.sidebar:
#     st.title('🤖💬 OpenAI Chatbot')
#     if 'OPENAI_API_KEY' in st.secrets:
#         st.success('API key already provided!', icon='✅')
#         openai.api_key = st.secrets['OPENAI_API_KEY']
#     else:
#         openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
#         if not (openai.api_key.startswith('sk-') and len(openai.api_key)==51):
#             st.warning('Please enter your credentials!', icon='⚠️')
#         else:
#             st.success('Proceed to entering your prompt message!', icon='👉')

# if valid_openai_key:
#     github_url = st.text_input("Github Link to public repo:")
#     repo_name = urlparse(github_url).path.split("/")[-1]
#     root_dir = os.path.join('./', repo_name)
#     st.write(root_dir)
#     # DB_PATH = os.path.join('./', f'db_{REPO_NAME}')
