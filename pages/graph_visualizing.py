import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from streamlit_agraph.config import Config, ConfigBuilder
from githubqa.get_info_from_api import github_api_call
from anytree import RenderTree 

if 'repo_url' not in st.session_state:
    st.session_state['repo_url'] = ""
else:
    repo_url  = st.session_state['repo_url']

# 이미지 온라인 링크 호스팅 : https://imgbb.com/ # 여기서 집어넣으면 댐
# 폴더 이미지 링크: https://i.ibb.co/9YC64Y4/folder.png
# Github Root 링크 : https://i.ibb.co/8MN42Hb/root.png
file_image_dict = {
    "py" : "https://i.ibb.co/HD532QV/py.png",
    "pdf" : "https://i.ibb.co/Gkptk9q/pdf.png",
    "txt" : "https://i.ibb.co/23mfJx3/txt.png",
    "ipynb": "https://i.ibb.co/nQ8yPfh/ipynb.png"
}

nodes, edges = [], []

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

# visualize_github_link = st.text_input("Github repository link을 입력해주세요")

if repo_url:
    nodes, edges = [], [] 
    nodes, edges = load_graph_data(repo_url)

    # 1. Build the config (with sidebar to play with options) .
    config_builder = ConfigBuilder(nodes)
    config = config_builder.build()

    # 2. If your done, save the config to a file.
    config.save("config.json")

    # 3. Simple reload from json file (you can bump the builder at this point.)
    config = Config(from_json="config.json")

    agraph(nodes=nodes, 
            edges=edges, 
            config=config)
else:
    st.error('Github repository를 선택해주세요.')