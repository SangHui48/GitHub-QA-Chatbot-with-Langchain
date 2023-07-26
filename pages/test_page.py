import requests
from common import *
from PIL import Image
from io import BytesIO
import streamlit as st
from githubqa.get_info_from_api import get_repo_list, get_avatar_info

initialize_session()
buy_me_tea()

st.session_state["user_name"] = st.text_input(
    'GitHub User:',  key="github_user_input_test_page", 
    value=st.session_state["user_name"],
    on_change=handling_user_change
    )

# print("user_name : ", st.session_state["user_name"])
# print("repo_name : ", st.session_state["repo_name"])
# print("github_url : ",st.session_state["repo_url"])

if st.session_state["user_name"]:
    user = st.session_state["user_name"]
    repo_list = get_repo_list(user) 
    user_info = get_avatar_info(user)
    if repo_list:
        repo_list = [DEFAULT_SELECT_VALUE] + repo_list 
        st.session_state["repo_name"] = st.selectbox(
                f"Select {user}'s repository", repo_list, 
                key="repo_select_test_page",
                index=repo_list.index(st.session_state["repo_name"]),
            )
        if st.session_state["repo_name"] != DEFAULT_SELECT_VALUE:
            st.session_state["repo_url"] = f"https://github.com/{st.session_state['user_name']}/{st.session_state['repo_name']}"
            print("user_name : ", st.session_state["user_name"])
            print("repo_name : ", st.session_state["repo_name"])
            print("repo_url : ",st.session_state["repo_url"])
    else:
        st.error("Invalid user ID")
