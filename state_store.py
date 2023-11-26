import streamlit as st
from enum import Enum
import copy


class State(Enum):
    ACCESS_TOKEN = "access_token"
    CHAT_HISTORY = "chat_history"
    CHAT_MESSAGES = "chat_messages"
    CURRENT_REPO = "current_repo"
    EXTENSION_FREQS = "extension_freqs"


REPO_STATES = [State.CHAT_HISTORY, State.CHAT_MESSAGES, State.CURRENT_REPO]

STATE_DEFAULTS = {
    State.ACCESS_TOKEN: -1,
    State.CHAT_HISTORY: "",
    State.CHAT_MESSAGES: [],
    State.CURRENT_REPO: None,
    State.EXTENSION_FREQS: {},
}


def init_states():
    if st.session_state:
        return
    for key, default in STATE_DEFAULTS.items():
        set_state(key, copy.deepcopy(default))


def is_default_init(key):
    return st.session_state[key] == STATE_DEFAULTS[key]


def set_state(key, value):
    st.session_state[key] = value


def get_state(key):
    return st.session_state[key]


def reset_current_repo_states():
    for key in REPO_STATES:
        set_state(key, copy.deepcopy(STATE_DEFAULTS[key]))
