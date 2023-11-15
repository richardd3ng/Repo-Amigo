import os
from urllib.parse import urlparse
import streamlit as st

from constants import DATA_ROOT, REPOS_DIR_NAME, DB_DIR_NAME
from embedder import Embedder
import file_utils

st.title('Repo Amigo - Your GitHub Chatbot!')

embedder = None
if github_url := st.text_input('GitHub Link to public repo:'):
    try:
        repo_name = urlparse(github_url).path.split("/")[-1]
        repo_path = os.path.join(DATA_ROOT, REPOS_DIR_NAME, repo_name)
        db_path = os.path.join(DATA_ROOT, DB_DIR_NAME, repo_name)

        with st.spinner('Cloning repo... (this may take a while depending on size)'):
            file_utils.clone_repo(github_url, repo_path)
        st.success('Succesfully cloned!')

        embedder = Embedder(repo_path, db_path)
        with st.spinner('Embedding documents...'):
            embedder.load_db()
        st.success('Ready for questions!')

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if question := st.text_input('Ask a question about the repo:'):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": question})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(question)
            # Display assistant response in chat message container
            answer = embedder.get_answer(question)
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(answer)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": answer})

    except Exception as e:
        st.error(f'Error: {e}')    


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
