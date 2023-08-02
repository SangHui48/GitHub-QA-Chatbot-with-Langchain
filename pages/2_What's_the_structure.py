import base64
import requests
from common import *
from PIL import Image
from io import BytesIO
import streamlit as st
from anytree import RenderTree 
from streamlit_agraph import agraph, Node, Edge, Config
from streamlit_agraph.config import Config
from githubqa.get_info_from_api import (
    github_api_call, get_repo_list, get_avatar_info
)

st.set_page_config(layout="wide", page_title="What's the Structure?")

initialize_session()
buy_me_tea()

### 확장자 -> 원하는 형식
# 목록이 너무 김. 따로 파일을 빼는게 나을지? 한 줄로 두는게 나을지?

## 그래프 아이콘
# https://github.com/PKief/vscode-material-icon-theme/tree/main#file-icons
# 일일이 추가 중. 정렬 아직 안함.
# 자동화하려면, 파일 확장자명과 위 링크 목록과 매칭 해야함. -> 조사 필요
file_image_dict = {
#   "확장자명" : "https://github.com/PKief/vscode-material-icon-theme/blob/main/icons/{이_부분}.svg"
#   root는 따로 핸들.
    "py" : "python", "pdf" : "pdf", "txt" : "text", 
    "dir" : "folder-resource", "file" : "lib",
    "ipynb": "python-misc", "exe" : "exe", "jpg" : "image",
    "jpeg" : "image", "png" : "image", "mp4" : "video", "webm":"video",
    "zip" : "zip", "txt" : "text", "md" : "markdown",
    "txt" : "document", "apk" : "android", "js" : "javascript",
    "json" : "json", "css" : "css", "html" : "html",
    "babelrc":"babel",  "scss":"sass", "webp" : "image",
    "gitignore":"git", "gitmodules":"git",
}

folder_image_set = set([
    'admin-open','admin','android-open','android','angular-open','angular','animation-open','animation','ansible-open','ansible','api-open','api','apollo-open','apollo','app-open','app','archive-open','archive','audio-open','audio','aurelia-open','aurelia','aws-open','aws','azure-pipelines-open','azure-pipelines','base-open','base','batch-open','batch','benchmark-open','benchmark','bower-open','bower','buildkite-open','buildkite','cart-open','cart','changesets-open','changesets','ci-open','ci','circleci-open','circleci','class-open','class','client-open','client','cluster-open','cluster','cobol-open','cobol','command-open','command','components-open','components','config-open','config','connection-open','connection','constant-open','constant','container-open','container','content-open','content','context-open','context','contract-open','contract','controller-open','controller','core-open','core','coverage-open','coverage','css-open','css','custom-open','custom','cypress-open','cypress','database-open','database','debug-open','debug','decorators-open','decorators','delta-open','delta','dist-open','dist','docker-open','docker','docs-open','docs','download-open','download','dump-open','dump','environment-open','environment','error-open','error','event-open','event','examples-open','examples','expo-open','expo','export-open','export','fastlane-open','fastlane','firebase-open','firebase','flow-open','flow','font-open','font','functions-open','functions','gamemaker-open','gamemaker','generator-open','generator','git-open','git','github-open','github','gitlab-open','gitlab','global-open','global','godot-open','godot','gradle-open','gradle','graphql-open','graphql','guard-open','guard','gulp-open','gulp','helper-open','helper','home-open','home','hook-open','hook','husky-open','husky','i18n-open','i18n','images-open','images','import-open','import','include-open','include','intellij-open','intellij-open_light','intellij','intellij_light','interface-open','interface','ios-open','ios','java-open','java','javascript-open','javascript','jinja-open','jinja-open_light','jinja','jinja_light','job-open','job','json-open','json','keys-open','keys','kubernetes-open','kubernetes','layout-open','layout','less-open','less','lib-open','lib','log-open','log','lua-open','lua','mail-open','mail','mappings-open','mappings','markdown-open','markdown','mercurial-open','mercurial','messages-open','messages','meta-open','meta','middleware-open','middleware','mjml-open','mjml','mobile-open','mobile','mock-open','mock','mojo-open','mojo','netlify-open','netlify','next-open','next','ngrx-actions-open','ngrx-actions','ngrx-effects-open','ngrx-effects','ngrx-entities-open','ngrx-entities','ngrx-reducer-open','ngrx-reducer','ngrx-selectors-open','ngrx-selectors','ngrx-state-open','ngrx-state','ngrx-store-open','ngrx-store','node-open','node','nuxt-open','nuxt','other-open','other','packages-open','packages','pdf-open','pdf','php-open','php','phpmailer-open','phpmailer','pipe-open','pipe','plastic-open','plastic','plugin-open','plugin','prisma-open','prisma','private-open','private','project-open','project','proto-open','proto','public-open','public','python-open','python','quasar-open','quasar','queue-open','queue','react-components-open','react-components','redux-actions-open','redux-actions','redux-reducer-open','redux-reducer','redux-selector-open','redux-selector','redux-store-open','redux-store','resolver-open','resolver','resource-open','resource','review-open','review','routes-open','routes','rules-open','rules','sass-open','sass','scala-open','scala','scripts-open','scripts','secure-open','secure','server-open','server','serverless-open','serverless','shader-open','shader','shared-open','shared','src-open','src','stack-open','stack','stencil-open','stencil','storybook-open','storybook','stylus-open','stylus','sublime-open','sublime','supabase-open','supabase','svelte-open','svelte','svg-open','svg','syntax-open','syntax','target-open','target','tasks-open','tasks','temp-open','temp','template-open','template','terraform-open','terraform','test-open','test','theme-open','theme','tools-open','tools','typescript-open','typescript','unity-open','unity','update-open','update','upload-open','upload','utils-open','utils','vercel-open','vercel','verdaccio-open','verdaccio','video-open','video','views-open','views','vm-open','vm','vscode-open','vscode','vue-directives-open','vue-directives','vue-open','vue','vuepress-open','vuepress','vuex-store-open','vuex-store','wakatime-open','wakatime','webpack-open','webpack','wordpress-open','wordpress','yarn-open','yarn'
])


## markdown 언어 리스트
# 위 dictionary와 완벽히 동일하지는 않음.
# https://github.com/react-syntax-highlighter/react-syntax-highlighter/blob/master/AVAILABLE_LANGUAGES_PRISM.MD
# 일일이 추가 중. 정렬 함.
# 자동화하려면, 파일 확장자명과 위 링크 목록과 아래 링크 매칭 해야함.
# -> https://github.com/jincheng9/markdown_supported_languages (최선의 링크인가)

file_type_dictionary = {
    "sh" : "bash", "ksh" : "bash", "bash" : "bash", "c" : "c", 
    "h" : "c", "cmake" : "cmake", "sh-session" : "console",
    "cpp" : "cpp", "c++" : "cpp", "cc" : "cpp", 
    "css" : "css", "diff" : "diff", "f" : "fortran",
    "go" : "go", "hs" : "haskell", "html" : "html",
    "htm" : "html", "ini" : "ini", "cfg" : "ini",
    "jade" : "jade", "java" : "java", "js" : "js",
    "jsp" : "jsp", "lua" : "lua", "mak" : "make",
    "md" : "markdown", "m" : "objectivec", "pl" : "perl",
    "pm" : "perl", "php" : "php", "py" : "python",
    "R" : "r", "scala" : "scala", "sql" : "sql",
    "sqlite3-console" : "sqlite3", "txt" : "text",
    "vim" : "vim", "vimrc" : "vim", "xml" : "xml",
    "xsl" : "xsl", "yaml" : "yaml", "yml" : "yaml",
}

def get_file_icon_url(file_extension):
    file_extension = file_extension.lower()
    if file_extension in file_image_dict:
        return f"https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/main/icons/{file_image_dict[file_extension]}.svg"
    else:
        return ""

def get_markdown_language_form(file_name):
    extension_name = file_name.split(".")[-1]
    extension_name = extension_name.lower()
    if extension_name in file_type_dictionary:
        return file_type_dictionary[extension_name]
    else:
        return None

      
nodes, edges = [], []

def load_graph_data(github_link):
    global file_image_dict, nodes, edges
    
    nodes, edges = [], [] 
    _, _ ,root,_ = github_api_call(github_link)

    for _, _, tmp_node in RenderTree(root):
        file_path = tmp_node.name
        file_name = tmp_node.name.split('/')[-1]
        
        if root.name == tmp_node.name:
            nodes.append(
                Node(id=file_path,
                    label=file_name,
                    title=file_name,
                    shape="circularImage",
                    image="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
                    link=github_link,
                    # size=100, # 이런 식으로 수정하면 됨.
                    color="white", 
                    )
                )
        elif "." in file_name or file_name=="LICENSE":  # LICENSE만 수동으로 핸들링. 개선 여지 존재?
            if file_name == "LICENSE":
                extension_name = ""
            else:
                extension_name = file_name.split(".")[-1]
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
            if file_name in folder_image_set:
                image_link = f"https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/main/icons/folder-{file_name}.svg"
            else:
                image_link = get_file_icon_url('dir')
            nodes.append(
                Node(
                    id=file_path,
                    label=file_name,
                    shape="circularImage",
                    image=image_link,
                    color="white"
                    )
                )  
        
        if tmp_node.parent:
            edges.append(
                Edge(source=tmp_node.parent.name, target=tmp_node.name, label="")
            )

    return nodes, edges


st.session_state["user_name"] = st.sidebar.text_input(
    'GitHub Username:',  key="github_user_input_sturcture", 
    value=st.session_state["user_name"],
    on_change=handling_user_change
    )
if st.session_state["user_name"]:
    user_name = st.session_state["user_name"]
    repo_list = get_repo_list(user_name)[0]
    user_info = get_avatar_info(user_name)
    if repo_list:
        repo_list = [DEFAULT_SELECT_VALUE] + repo_list 
        st.session_state["repo_name"] = st.sidebar.selectbox(
                f"Select {user_name}'s repository:", repo_list, 
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
        st.error("Invalid username")


if st.session_state['repo_url']:
    st.markdown("<code><h2 style='text-align: center;padding:15px;margin-bottom:10px ;color: #04A930;'>Repo Structure Visualization</h2></code>", 
        unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="small")
    nodes, edges = [], [] 
    nodes, edges = load_graph_data(st.session_state['repo_url'])

    radiobutton_config = st.sidebar.radio(
                            "Layout",
                            ('Physics', 'Hierarchical'),
                        )
    if radiobutton_config == 'Physics':
        config_physics = True
        config_hierarchical = False
    else:
        config_physics = False
        config_hierarchical = True
 
    config = Config(
                width=col1.width, height=750,
                directed=True, physics=config_physics, 
                hierarchical=config_hierarchical, # **kwargs
            )

    with col1:
        agraph(nodes=nodes, edges=edges, config=config)
    
    user, repo = st.session_state['repo_url'].split('/')[-2:]
    with col2:
        # key : file_path , value : content 
        total_repo_file_info_dict, _ ,_,_ = github_api_call(st.session_state['repo_url'])
        repo_list = [DEFAULT_SELECT_VALUE]  + list(total_repo_file_info_dict.keys())
        file_name = st.selectbox(
                f"Select {repo}'s filename",
                repo_list, key="what_is_structure_repo_name"
        )
        if file_name != DEFAULT_SELECT_VALUE:
            st.code(
                total_repo_file_info_dict[file_name],
                language=get_markdown_language_form(file_name),
                line_numbers=True
            )
        else:
            pass # 공백.
            # st.info("select your file_name")
else:
    st.info('Please input **Username** and **name of the repository**.')
