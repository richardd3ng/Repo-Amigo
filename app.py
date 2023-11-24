import os
from urllib.parse import urlparse
import streamlit as st
from streamlit_oauth import OAuth2Component

from constants import (
    CLIENT_ID,
    CLIENT_SECRET,
    GITHUB_AUTHORIZATION_URL,
    GITHUB_TOKEN_URL,
    REDIRECT_URI,
    DATA_ROOT,
    REPOS_DIR_NAME,
    DB_DIR_NAME,
)
from embedder import Embedder
from questions import QuestionContext, get_answer
import file_utils

st.title("Repo Amigo - Your GitHub Chatbot!")

print("HELLO!!!!!!!!!!!!!!!!!!2")

oauth2 = OAuth2Component(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    authroize_endpoint=GITHUB_AUTHORIZATION_URL,
    token_endpoint=GITHUB_TOKEN_URL,
    refresh_token_endpoint=None,
    revoke_token_endpoint=None,
)

if "access_token" not in st.session_state:
    result = oauth2.authorize_button(
        "Login with GitHub", redirect_uri=REDIRECT_URI, scope=""
    )
    if result and "token" in result:
        st.session_state["access_token"] = result["token"]["access_token"]
        st.rerun()
else:
    access_token = st.session_state["access_token"]
    print(f"found token: {access_token}")
    if github_url := st.text_input("GitHub Link (must be public)"):
        try:
            repo_name = urlparse(github_url).path.split("/")[-1]
            repo_path = os.path.join(DATA_ROOT, REPOS_DIR_NAME, repo_name)
            print(f"repo_name: {repo_name}")
            print(f"repo_path: {repo_path}")

            db_path = os.path.join(DATA_ROOT, DB_DIR_NAME, repo_name)

            with st.spinner(
                f"Cloning {repo_name}... (this may take a while depending on size)"
            ):
                file_utils.clone_repo(github_url, repo_path, access_token)

            embedder = Embedder(repo_path, db_path)
            with st.spinner(
                f"Embedding documents for {repo_name}... (this may take a while depending on size)"
            ):
                embedder.load_db()
            st.success(f"Ready for questions about {repo_name}!")

            if "messages" not in st.session_state:
                st.session_state["messages"] = []
            for message in st.session_state["messages"]:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if question := st.chat_input(
                f"What do you want to know about {repo_name}?"
            ):
                st.session_state["messages"].append(
                    {"role": "user", "content": question}
                )
                with st.chat_message("user"):
                    st.markdown(question)
                with st.spinner("Thinking..."):
                    if "chat_history" not in st.session_state:
                        st.session_state["chat_history"] = ""

                    context = QuestionContext(
                        repo_name,
                        github_url,
                        st.session_state["chat_history"],
                        st.session_state["extension_freqs"],
                    )
                    answer = get_answer(question, context, embedder.retriever)
                    st.session_state[
                        "chat_history"
                    ] += f"Question: {question}\nAnswer: {answer}\n"

                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    message_placeholder.markdown(answer)
                st.session_state["messages"].append(
                    {"role": "assistant", "content": answer}
                )
                print(f"message_history: {st.session_state['messages']}")

        except Exception as e:
            st.error(f"Error: {e}")
