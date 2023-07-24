import streamlit as st
from githubqa.get_info_from_api import get_repo_list

DEFAULT_SELECT_VALUE = "Select Repo"
MODEL_NAME = "gpt-3.5-turbo-16k"

def initialize_session():
    if not "initialized" in st.session_state:
        st.session_state["initialized"] = True
        st.session_state["repo_name"] = DEFAULT_SELECT_VALUE
        st.session_state["user_name"] = ""
        st.session_state["repo_url"] = ""
        st.session_state["visitied_list"] = []
        st.session_state["messages"] = []


def handling_user_change():
    st.session_state["repo_name"] = DEFAULT_SELECT_VALUE
    st.session_state["repo_url"] = ""
    