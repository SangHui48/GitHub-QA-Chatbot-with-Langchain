import os
import base64
import requests
import streamlit as st

st.set_page_config(layout="wide")

@st.cache_data()
def get_github_content(user, repo, path=''):
    url = f'https://api.github.com/repos/{user}/{repo}/contents/{path}'
    response = requests.get(url, auth=(os.getenv("GITHUB_NAME"),os.getenv("GITHUB_TOKEN")))
    return response.json()

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
            
def print_content(url, file_type):
    response = requests.get(url,  auth=(st.secrets["GITHUB_NAME"], st.secrets["GITHUB_TOKEN"])).json()
    content = base64.b64decode(response['content']).decode()
    with col2:
        st.code(content, language=file_type, line_numbers=True)

def get_file_type(file_name): # 현재 .md, .py, .js만 호환
    # https://github.com/react-syntax-highlighter/react-syntax-highlighter/blob/master/AVAILABLE_LANGUAGES_PRISM.MD
    if file_name.endswith(".md"):
        file_type = "markdown"
    elif file_name.endswith(".py"):
        file_type = "python"
    elif file_name.endswith(".js"):
        file_type = "javascript"
    else:
        file_type = None

    return file_type

col1, col2 = st.columns([1,4])

with col1:
    user = st.text_input('GitHub User:')
    repo = st.text_input('GitHub Repo:')

    if user and repo:
        print_directory_structure(user, repo)
