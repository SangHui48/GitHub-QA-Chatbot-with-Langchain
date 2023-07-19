import requests
import streamlit as st
import os
from dotenv import load_dotenv
import base64

load_dotenv()

@st.cache_data()
def get_github_content(user, repo, path=''):
    url = f'https://api.github.com/repos/{user}/{repo}/contents/{path}'
    response = requests.get(url, auth=("GITHUB_NAME","GITHUB_TOKEN"))
    return response.json()

def print_directory_structure(user, repo, path='', depth=0):
    contents = get_github_content(user, repo, path)

    if type(contents) == "list":
        if "message" in contents[0].keys(): # Still testing
            if contents["message"].startswith("API rate limit exceeded for"):
                print("ERROR: API rate limit exceeded!")
                st.write("ERROR: API rate limit exceeded!")

    for item in contents:
        if item['type'] == 'dir':
            st.write("-"*(depth+1) + f'Directory: {item["path"]}')
            print_directory_structure(user, repo, item['path'], depth+1)
        else:
            #st.write("- "*(depth+1) + " "*bool(depth) + f' File: {item["path"]}')
            st.write(f'File: {item["path"]}') #"<a href='#' id='my-link'>Click me</a>"
            #if st.button("my-link"):
            #    st.write("Link clicked!")
            print_content(item["_links"]['self'])
            
def print_content(url):
    response = requests.get(url, auth=("GITHUB_NAME","GITHUB_TOKEN")).json()
    content = base64.b64decode(response['content']).decode()
    # content = content[2:-1].replace('\\n', '\n')
    with col2:
        st.code(content, language='python', line_numbers=True)

col1, col2 = st.columns(2)

with col1:
    user = st.text_input('GitHub User:', 'SamLynnEvans')
    repo = st.text_input('GitHub Repo:', 'Transformer')

    if user and repo:
        print_directory_structure(user, repo)
