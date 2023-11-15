import os
import shutil
import subprocess
import uuid
from collections import defaultdict
from urllib.parse import urlparse
import streamlit as st
import file_utils

st.title('Repo Amigo - Your GitHub Chatbot!')


if github_url := st.text_input('GitHub Link to public repo:'):
    try:
        repo_name = urlparse(github_url).path.split("/")[-1]
        repo_path = os.path.join("./", repo_name)
        with st.spinner('Cloning repo... (this may take a while depending on size)'):
            file_utils.clone_repo(github_url, repo_path)
        st.success('Succesfully cloned!')
    except Exception as e:
        st.error(f'Invalid GitHub URL: {e}')

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
