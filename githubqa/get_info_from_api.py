import os
import time
import json
import base64
import requests
from dotenv import load_dotenv
from anytree import Node, RenderTree 
from langchain.document_loaders import PyPDFLoader
import streamlit as st

API_CALL_COUNT = 0
TOTAL_INFO_DICT = {}
STRUCTURE_CONTENT = ''
GITHUB_NAME = st.secrets['GITHUB_NAME']
GITHUB_TOKEN = st.secrets['GITHUB_TOKEN']

# .env 파일 로드
load_dotenv()

ROOT = Node("root")

def api_call(api_link):
    global API_CALL_COUNT
    API_CALL_COUNT += 1

    response = requests.get(
        api_link,
        auth=( GITHUB_NAME , GITHUB_TOKEN)
    )

    if response.status_code == 200:
        content = response.content.decode('utf-8')
        print(api_link)
        return json.loads(content)
    else:
        print(response.status_code)
        return None
    
    
def get_dir_info(api_link, file_name="Git_Repository", parent_node=ROOT):
    file_info_list = api_call(api_link)
    for file_info in file_info_list:
        will_pass = False
        file_name = file_info["name"]
        if file_name.endswith(('.jpg', '.png','jpeg','.txt')):
            will_pass = True
        elif file_name.endswith('.pdf'):
            file_pdf_link = file_info["download_url"]
            loader = PyPDFLoader(file_pdf_link)
            pages = loader.load()
            total_pdf_string = ""
            for page in pages:
                total_pdf_string += page.page_content
            TOTAL_INFO_DICT[file_name] = total_pdf_string
            will_pass = True
        elif file_name.endswith('.txt'):
            file_txt_link = file_info["download_url"]
            response = requests.get(file_txt_link)
            TOTAL_INFO_DICT[file_name] = response.text
            will_pass = True
        else:
            file_api_link = file_info["_links"]["self"]

        if will_pass==True:
          Node(file_name, parent=parent_node)
          continue

        if file_info["type"] == "file":
            file_info = api_call(file_api_link)
            Node(file_name, parent=parent_node)
            content = base64.b64decode(file_info['content']).decode('utf-8')
            TOTAL_INFO_DICT[file_name] = content
        elif file_info["type"] == "dir":
            dir_node = Node(file_name, parent=parent_node)
            get_dir_info(file_api_link, file_name, dir_node)

@st.cache_data()
def github_api_call(web_link):
    start_time = time.time()
    user_name, repo_name = web_link.split('/')[-2:]
    get_dir_info(f"https://api.github.com/repos/{user_name}/{repo_name}/contents/")

    end_time = time.time()  # 실행 종료 시간 기록
    execution_time = end_time - start_time  # 실행 시간 계산
    print(f"프로그램 실행 시간: {execution_time:.2f}초")
    print(f"API call 횟수 : {API_CALL_COUNT}")
    
    tree_structure = ""
    for pre, _, node in RenderTree(ROOT):
        tree_structure += f"{pre}{node.name}\n"
    
    STRUCTURE_CONTENT = f'''
    {user_name} 's github link is {repo_name} and the {repo_name}'s github folder structure is like that.

    {tree_structure}
    '''
    
    return TOTAL_INFO_DICT, STRUCTURE_CONTENT
