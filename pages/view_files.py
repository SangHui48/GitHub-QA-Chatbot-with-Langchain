import os
import base64
import requests
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from streamlit_agraph.config import Config, ConfigBuilder
from githubqa.get_info_from_api import github_api_call
from anytree import RenderTree 


### File viewer

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
    with col3:
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

### Graph visualization

# 이미지 온라인 링크 호스팅 : https://imgbb.com/ # 여기서 집어넣으면 댐
# 폴더 이미지 링크: https://i.ibb.co/9YC64Y4/folder.png
# Github Root 링크 : https://i.ibb.co/8MN42Hb/root.png
file_image_dict = {
    "py" : "https://i.ibb.co/HD532QV/py.png",
    "pdf" : "https://i.ibb.co/Gkptk9q/pdf.png",
    "txt" : "https://i.ibb.co/23mfJx3/txt.png",
    "ipynb": "https://i.ibb.co/nQ8yPfh/ipynb.png"
}

def load_graph_data(github_link):
    global file_image_dict, nodes, edges
    
    nodes, edges = [], [] 
    
    _, _ ,root = github_api_call(github_link)

    for _, _, tmp_node in RenderTree(root):
        file_name = github_link.split('/')[-1]
        # print(tmp_node.name)
        if tmp_node.name == root.name:
            nodes.append(
                Node(id=tmp_node.name,
                    label=file_name,
                    title=file_name,
                    shape="circularImage",
                    image="https://i.ibb.co/8MN42Hb/root.png",
                    link=github_link,
                    # size=100, # 이런 식으로 수정하면 됨.
                    # color="#FF0000", 
                    )
                )
        elif "." in tmp_node.name or tmp_node.name=="LICENSE":  
            if tmp_node.name == "LICENSE":
                extension_name = ""
            else:
                extension_name = tmp_node.name.split(".")[1]
            image_link = "https://i.ibb.co/T0jg7QZ/file.png"
            if extension_name in file_image_dict:
                 image_link = file_image_dict[extension_name]
            nodes.append(
                Node(id=tmp_node.name,
                    label=tmp_node.name,
                    shape="circularImage",
                    image=image_link,
                    )
                )
        else:
            nodes.append(
                Node(id=tmp_node.name,
                    label=tmp_node.name,
                    shape="circularImage",
                    image="https://i.ibb.co/9YC64Y4/folder.png"
                    )
                )  
        
        if tmp_node.parent:
            edges.append(
                Edge(source=tmp_node.parent.name, target=tmp_node.name, label="")
            )

    return nodes, edges

### Input

st.set_page_config(layout="wide")
col1, col2, col3 = st.columns([1,3,3])

if 'repo_url' not in st.session_state:
    st.session_state['repo_url'] = ""
else:
    repo_url = st.session_state['repo_url']

if st.session_state['repo_url']:
    with col1:
        user, repo = st.session_state['repo_url'].split('/')[-2:]
        print_directory_structure(user, repo)

    with col2:
        nodes, edges = [], [] 
        nodes, edges = load_graph_data(repo_url)

        # 1. Build the config (with sidebar to play with options) .
        config_builder = ConfigBuilder(nodes)
        config = config_builder.build()

        # 2. If your done, save the config to a file.
        config.save("config.json")

        # 3. Simple reload from json file (you can bump the builder at this point.)
        config = Config(from_json="config.json")

        return_value = agraph(nodes=nodes, 
                                edges=edges, 
                                config=config)
        
        st.write(return_value)
else:
    st.error('Please check Username and Repository name.')