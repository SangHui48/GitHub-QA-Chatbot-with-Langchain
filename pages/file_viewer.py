import base64
import requests
from common import *
import streamlit as st
from githubqa.get_info_from_api import get_github_content

initialize_session()
buy_me_tea()

file_type_dictionary = {
    ".md" : "markdown",
    ".py" : "python",
    ".js" : "javascript"
}

def print_content(url, file_type):
    response = requests.get(url,  auth=(st.secrets["GITHUB_NAME"], st.secrets["GITHUB_TOKEN"])).json()
    try:
        content = base64.b64decode(response['content']).decode('utf-8')
        with col2:
            st.code(content, language=file_type, line_numbers=True)
    except:
        st.code("Cannot read this file_content", language="markdown", line_numbers=True)
    



st.session_state["user_name"] = st.text_input(
    'GitHub User:',  key="github_user_input", 
    value=st.session_state["user_name"],
    on_change=handling_user_change
    )
if st.session_state["user_name"]:
    user = st.session_state["user_name"]
    repo_list = get_repo_list(user)
    if repo_list:
        repo_list = [DEFAULT_SELECT_VALUE] + repo_list 
        st.session_state["repo_name"] = st.selectbox(
                f"Select {user}'s repository", repo_list, 
                key="repo_select",
                index=repo_list.index(st.session_state["repo_name"]),
            )
        if st.session_state["repo_name"] != DEFAULT_SELECT_VALUE:
            st.session_state["repo_url"] = f"https://github.com/{st.session_state['user_name']}/{st.session_state['repo_name']}"
    else:
        st.error("Invalid user ID")



def print_directory_structure(user, repo, path='', depth=0):
    contents = get_github_content(user, repo, path)

    # GitHub API 제한 핸들링
    try:
        if contents["message"].startswith("API rate limit exceeded for"):
            print("ERROR: API rate limit exceeded!")
            st.write("ERROR: API rate limit exceeded!")
    except:
        pass # 핸들링 안하는 중

    for item in contents:
        if item['type'] == 'dir':
            print_directory_structure(user, repo, item['path'], depth+1)
        else:
            if st.button(item['path']):
                print_content(item['_links']['self'], get_file_type(item['path']))
            


def get_file_type(file_name): # 현재 .md, .py, .js만 호환
    # https://github.com/react-syntax-highlighter/react-syntax-highlighter/blob/master/AVAILABLE_LANGUAGES_PRISM.MD
    extension_name = "." + file_name.split(".")[-1]
    if extension_name in file_type_dictionary:
        return file_type_dictionary[extension_name]
    else:
        return None
    
st.title('`Repo Structure Visualization`')
col1, col2 = st.columns([1,4])
if st.session_state['repo_url']:
    user, repo = st.session_state['repo_url'].split('/')[-2:]
    with col1:
        print_directory_structure(user, repo)
else:
    st.info('Please insert your name and repo_name')