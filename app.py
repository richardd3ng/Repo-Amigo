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
from state_store import (
    State,
    init_states,
    is_default_init,
    get_state,
    set_state,
    reset_current_repo_states,
)
import file_utils

init_states()
st.title("Repo Amigo - Your GitHub Chatbot!")

if is_default_init(State.ACCESS_TOKEN):
    oauth2 = OAuth2Component(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        authroize_endpoint=GITHUB_AUTHORIZATION_URL,
        token_endpoint=GITHUB_TOKEN_URL,
        refresh_token_endpoint=None,
        revoke_token_endpoint=None,
    )
    result = oauth2.authorize_button(
        "Login with GitHub", redirect_uri=REDIRECT_URI, scope=""
    )
    if result and "token" in result:
        set_state(State.ACCESS_TOKEN, result["token"]["access_token"])
        st.rerun()
else:
    access_token = get_state(State.ACCESS_TOKEN)
    print(f"found token: {access_token}")
    if github_url := st.text_input("GitHub Link (must be public)"):
        try:
            repo_name = urlparse(github_url).path.split("/")[-1]
            repo_path = os.path.join(DATA_ROOT, REPOS_DIR_NAME, repo_name)
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
                # pass
            st.success(f"Ready for questions about {repo_name}!")

            if get_state(State.CURRENT_REPO) != github_url:
                reset_current_repo_states()
            set_state(State.CURRENT_REPO, github_url)

            for message in get_state(State.CHAT_MESSAGES):
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if question := st.chat_input(
                f"What do you want to know about {repo_name}?"
            ):
                get_state(State.CHAT_MESSAGES).append(
                    {"role": "user", "content": question}
                )
                with st.chat_message("user"):
                    st.markdown(question)
                with st.spinner("Thinking..."):
                    context = QuestionContext(
                        repo_name,
                        github_url,
                        get_state(State.EXTENSION_FREQS),
                    )
                    answer = get_answer(question, context, embedder.retriever)

                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    message_placeholder.markdown(answer)
                get_state(State.CHAT_MESSAGES).append(
                    {"role": "assistant", "content": answer}
                )

        except Exception as e:
            st.error(f"Error: {e}")
