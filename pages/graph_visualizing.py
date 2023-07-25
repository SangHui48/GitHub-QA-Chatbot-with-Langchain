from common import *
import streamlit as st
from anytree import RenderTree 
from streamlit_agraph import agraph, Node, Edge, Config
from streamlit_agraph.config import Config, ConfigBuilder
from githubqa.get_info_from_api import github_api_call, get_repo_list

# Online Image link Hosting : https://imgbb.com/
# Folder image link : https://i.ibb.co/9YC64Y4/folder.png
# Github root link : https://i.ibb.co/8MN42Hb/root.png

initialize_session()

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
def get_file_icon_url(file_extension):
    if file_extension in file_image_dict:
        return f"https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/main/icons/{file_image_dict[file_extension.lower()]}.svg"
    else:
        return ""


nodes, edges = [], []

def load_graph_data(github_link):
    global file_image_dict, nodes, edges
    
    nodes, edges = [], [] 
    _, _ ,root = github_api_call(github_link)

    for _, _, tmp_node in RenderTree(root):
        file_path = tmp_node.name
        file_name = tmp_node.name.split('/')[-1]
        node_id = tmp_node.name

        if root.name == tmp_node.name:
            nodes.append(
                Node(id=file_path,
                    label=file_name,
                    title=file_name,
                    shape="circularImage",
                    image=get_file_icon_url('root'),
                    link=github_link,
                    size=30, # 이런 식으로 수정하면 됨.
                    color="#FFFFFF", 
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
                    id=file_path,
                    label=file_name,
                    shape="circularImage",
                    image=image_link,
                    color = "#FFFFFF",
                    )
                )
        else:
            nodes.append(
                Node(
                    id=file_path,
                    label=file_name,
                    shape="circularImage",
                    image=get_file_icon_url('dir'),
                    color = "#FFFFFF",
                    )
                )  
        
        if tmp_node.parent:
            edges.append(
                Edge(source=tmp_node.parent.name, target=tmp_node.name, label="")
            )

    return nodes, edges


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


if st.session_state['repo_url'] != "":
    nodes, edges = [], [] 
    nodes, edges = load_graph_data(st.session_state['repo_url'])

    # 1. Build the config (with sidebar to play with options) .
    config_builder = ConfigBuilder(nodes)
    config = config_builder.build()

    # 2. If your done, save the config to a file.
    config.save("config.json")

    # 3. Simple reload from json file (you can bump the builder at this point.)
    config = Config(from_json="config.json")
    # config.physics = True
    # config.hierarchical = False # True가 이상하게 안됨.
    # config.width = 1000
    # config.height = 1000
    

    agraph(nodes=nodes, 
            edges=edges, 
            config=config)
else:
    st.info('Github 정보를 입력해주세요.')