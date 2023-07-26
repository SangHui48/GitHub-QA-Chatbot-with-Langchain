import base64
import requests
from common import *
from PIL import Image
from io import BytesIO
import streamlit as st
from anytree import RenderTree 
from streamlit_agraph import agraph, Node, Edge, Config
from streamlit_agraph.config import Config, ConfigBuilder
from githubqa.get_info_from_api import (
    github_api_call, get_repo_list, 
    get_avatar_info, get_github_content
)

st.set_page_config(layout="wide", page_title="What's the Structure")

initialize_session()
buy_me_tea()

## Get file icons
# https://github.com/PKief/vscode-material-icon-theme/tree/main#file-icons
file_image_dict = { # 추가 중. 정렬 아직 안함.
    "py" : "python",
    "pdf" : "pdf",
    "txt" : "text",
    "dir" : "folder-resource",
    "file" : "lib",
    "root" : "git",
    "ipynb": "python-misc",
    "exe" : "exe",
    "jpg" : "image",
    "jpeg" : "image",
    "png" : "image",
    "mp4" : "video",
    "zip" : "zip",
    "txt" : "text",
    "md" : "markdown",
    "txt" : "document",
    
}

# 위 dictionary와 동일할지는 알아봐야함.
file_type_dictionary = {
    ".md" : "markdown",
    ".py" : "python",
    ".js" : "javascript"
}

def get_file_icon_url(file_extension):
    if file_extension in file_image_dict:
        return f"https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/main/icons/{file_image_dict[file_extension.lower()]}.svg"
    else:
        return ""


nodes, edges = [], []

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
    if extension_name in file_image_dict:
        return file_image_dict[extension_name]
    else:
        return None
    
def print_content(url, file_type):
    response = requests.get(url,  auth=(st.secrets["GITHUB_NAME"], st.secrets["GITHUB_TOKEN"])).json()
    try:
        content = base64.b64decode(response['content']).decode('utf-8')
        with col2:
            st.code(content, language=file_type, line_numbers=True)
    except:
        st.code("Cannot read this file_content", language="markdown", line_numbers=True)
    

def load_graph_data(github_link):
    global file_image_dict, nodes, edges
    
    nodes, edges = [], [] 
    _, _ ,root = github_api_call(github_link)

    for _, _, tmp_node in RenderTree(root):
        file_path = tmp_node.name
        file_name = tmp_node.name.split('/')[-1]
        
        if root.name == tmp_node.name:
            nodes.append(
                Node(id=file_path,
                    label=file_name,
                    title=file_name,
                    shape="circularImage",
                    image=get_file_icon_url('root'),
                    link=github_link,
                    # size=100, # 이런 식으로 수정하면 됨.
                    color="white", 
                    )
                )
        elif "." in file_name or file_name=="LICENSE":  
            if file_name == "LICENSE":
                extension_name = ""
            else:
                extension_name = file_name.split(".")[1]
            image_link = get_file_icon_url('file')
            if extension_name in file_image_dict:
                 image_link = get_file_icon_url(extension_name)
            nodes.append(
                Node(
                    id=file_path, label=file_name,
                    shape="circularImage",
                    image=image_link, color="white",
                    )
                )
        else:
            nodes.append(
                Node(
                    id=file_path,
                    label=file_name,
                    shape="circularImage",
                    image=get_file_icon_url('dir'),
                    color="white"
                    )
                )  
        
        if tmp_node.parent:
            edges.append(
                Edge(source=tmp_node.parent.name, target=tmp_node.name, label="")
            )

    return nodes, edges


st.session_state["user_name"] = st.sidebar.text_input(
    'GitHub User:',  key="github_user_input_sturcture", 
    value=st.session_state["user_name"],
    on_change=handling_user_change
    )
if st.session_state["user_name"]:
    user_name = st.session_state["user_name"]
    repo_list = get_repo_list(user_name)
    user_info = get_avatar_info(user_name)
    if repo_list:
        repo_list = [DEFAULT_SELECT_VALUE] + repo_list 
        st.session_state["repo_name"] = st.sidebar.selectbox(
                f"Select {user_name}'s repository", repo_list, 
                key="repo_select_graph_visualize",
                index=repo_list.index(st.session_state["repo_name"]),
            )
        if st.session_state["repo_name"] != DEFAULT_SELECT_VALUE:
            st.session_state["repo_url"] = f"https://github.com/{st.session_state['user_name']}/{st.session_state['repo_name']}"
        avatar_url = user_info['avatar_url']
        image_response = requests.get(avatar_url)
        image = Image.open(BytesIO(image_response.content)).resize((250,250))
        st.sidebar.image(image, use_column_width='always', caption=f"{user_name}'s profile")
    else:
        st.error("Invalid user ID")


if st.session_state['repo_url'] != "":
    st.markdown("<code><h2 style='text-align: center;padding:15px;margin-bottom:10px ;color: #04A930;'>Repo Structure Visualization</h2></code>", 
        unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="small")
    nodes, edges = [], [] 
    nodes, edges = load_graph_data(st.session_state['repo_url'])
    config = Config(
        width=col1.width, height=750,
        directed=True, physics=True, 
        hierarchical=False, # **kwargs
    )
    with col1:
        agraph(nodes=nodes, edges=edges, config=config)
    
    
    # col1, col2 = st.columns([1,4])
    
    user, repo = st.session_state['repo_url'].split('/')[-2:]
    with col2:
        # key : file_path , value : content 
        total_repo_file_info_dict, _ ,_ = github_api_call(st.session_state['repo_url'])
        repo_list = [DEFAULT_SELECT_VALUE]  + list(total_repo_file_info_dict.keys())
        file_name = st.selectbox(
                f"Select {repo}'s filename",
                repo_list, key="what_is_structure_repo_name"
        )
        if file_name != DEFAULT_SELECT_VALUE:
            file_extension = get_file_type(file_name)
            st.code(total_repo_file_info_dict[file_name], language=file_extension, line_numbers=True)
        else:
            st.info("select your file_name")
        # print_directory_structure(user, repo)
else:
    st.info('Please insert your name and repo_name')
#     # 1. Build the config (with sidebar to play with options) .
#     config_builder = ConfigBuilder(nodes)
#     config = config_builder.build()

#     # 2. If your done, save the config to a file.
#     config.save("config.json")

#     # 3. Simple reload from json file (you can bump the builder at this point.)
#     config = Config(from_json="config.json")

