import time
import json
import base64
import requests
import streamlit as st
from anytree import Node, RenderTree
from langchain.document_loaders import PyPDFLoader


API_CALL_COUNT = 0
TOTAL_INFO_DICT = {}
ROOT = None


@st.cache_data()
def get_avatar_info(user_name):
    # name : 닉네임 , public_repos , avatar_url
    url = f'https://api.github.com/users/{user_name}'
    response = requests.get(url,auth=(st.secrets["GITHUB_NAME"], st.secrets["GITHUB_TOKEN"]))
    return response.json()
    
    
@st.cache_data()
def get_repo_list(user_name):
    user_repos = []
    
    url = f'https://api.github.com/users/{user_name}/repos'
    response = requests.get(url,auth=(st.secrets["GITHUB_NAME"], st.secrets["GITHUB_TOKEN"]))
    if response.status_code == 200:
        for tmp_dict in response.json():
            user_repos.append(tmp_dict['name'])
        return user_repos
    else:
        return None


def api_call(api_link):
    global API_CALL_COUNT
    API_CALL_COUNT += 1

    response = requests.get(
        api_link,
        auth=(st.secrets["GITHUB_NAME"], st.secrets["GITHUB_TOKEN"])
    )

    if response.status_code == 200:
        content = response.content.decode('utf-8')
        print(api_link)
        return json.loads(content)
    else:
        print(response.status_code)
        return None


def get_dir_info(api_link, path_name, parent_node ):
    # print(api_link, path_name, parent_node)
    file_info_list = api_call(api_link)
    for file_info in file_info_list:
        will_pass = False
        file_name = file_info["name"]
        next_path_name = path_name + "/" + file_name
        if file_name.endswith(('.jpg', '.png','jpeg','.txt', '.gif', '.ico','.webp')):
            will_pass = True
        elif file_name.endswith('.pdf'):
            file_pdf_link = file_info["download_url"]
            loader = PyPDFLoader(file_pdf_link)
            pages = loader.load()
            total_pdf_string = ""
            for page in pages:
                total_pdf_string += page.page_content
            TOTAL_INFO_DICT[next_path_name] = total_pdf_string
            will_pass = True
        elif file_name.endswith('.txt'):
            file_txt_link = file_info["download_url"]
            response = requests.get(file_txt_link)
            TOTAL_INFO_DICT[next_path_name] = response.text
            will_pass = True
        else:
            file_api_link = file_info["_links"]["self"]

        if will_pass==True:
          Node(next_path_name, parent=parent_node)
          continue

        if file_info["type"] == "file":
            file_info = api_call(file_api_link)
            Node(next_path_name, parent=parent_node)
            try:
                content = base64.b64decode(file_info['content']).decode('utf-8')
            except:
                print("cannot read", file_name)
                content = ""
            TOTAL_INFO_DICT[next_path_name] = content
        elif file_info["type"] == "dir":
            if file_name in ["node_modules"]:
                continue
            dir_node = Node(next_path_name, parent=parent_node)
            get_dir_info(file_api_link, next_path_name, dir_node)


@st.cache_data()
def github_api_call(web_link):
    global ROOT,API_CALL_COUNT,TOTAL_INFO_DICT

    user_name, repo_name = web_link.split('/')[-2:]

    ROOT = Node(repo_name)
    API_CALL_COUNT = 0
    TOTAL_INFO_DICT = {}

    start_time = time.time()

    get_dir_info(
        api_link=f"https://api.github.com/repos/{user_name}/{repo_name}/contents/",
        path_name=repo_name,
        parent_node=ROOT
    )

    end_time = time.time()  # 실행 종료 시간 기록
    execution_time = end_time - start_time  # 실행 시간 계산
    print(f"프로그램 실행 시간: {execution_time:.2f}초")
    print(f"API call 횟수 : {API_CALL_COUNT}")

    tree_structure = ""
    for pre, _, node in RenderTree(ROOT):
        file_name = node.name.split("/")[-1]
        tree_structure += f"{pre}{file_name}\n"
        
    # print(tree_structure)
    structure_content = f'''
    {user_name} 's github link is {repo_name} and the {repo_name}'s github folder structure is like that.
    
    {tree_structure}
    '''

        
    email = get_avatar_info(user_name)['email']
    repo_list = [repo for repo in get_repo_list(user_name)]
    repo_structure = ""
    for pre, _, node in RenderTree(ROOT):
        file_name = node.name.split("/")[-1]
        repo_structure += f"{pre}{repo_list}\n"

    followers = get_followers(user_name)
    user_content = f'''
    {user_name}’s email is {email}.
    {user_name}’s followers are {followers}.
    {user_name}’s other repositories have {repo_structure}.
    If you want to know about other repository content, change your repository selection.
    '''
    return TOTAL_INFO_DICT, structure_content, ROOT, user_content



@st.cache_data()
def get_github_content(user, repo, path=''):
    url = f'https://api.github.com/repos/{user}/{repo}/contents/{path}'
    response = requests.get(url, auth=(st.secrets["GITHUB_NAME"], st.secrets["GITHUB_TOKEN"]))
    return response.json()



@st.cache_data(show_spinner=False)
def get_language_list(user_name,repo_name):
    user_repos = []
    
    url = f'https://api.github.com/repos/{user_name}/{repo_name}/languages'
    response = requests.get(url,auth=(st.secrets["GITHUB_NAME"], st.secrets["GITHUB_TOKEN"]))
    if response.status_code == 200:
        for tmp_dict in response.json():
            user_repos.append(tmp_dict)
        return user_repos
    else:
        return None
    
@st.cache_data(show_spinner=False)
def get_contributors(user_name,repo_name):
    user_repos = []
    html_repos = []
    
    url = f'https://api.github.com/repos/{user_name}/{repo_name}/contributors'
    response = requests.get(url,auth=(st.secrets["GITHUB_NAME"], st.secrets["GITHUB_TOKEN"]))
    if response.status_code == 200:
        for tmp_dict in response.json():
            user_repos.append(tmp_dict['login'])
            html_repos.append(tmp_dict['html_url'])
        return user_repos, html_repos
    else:
        return None

    
@st.cache_data(show_spinner=False)
def get_forks(user_name,repo_name):
    url = f'https://api.github.com/repos/{user_name}/{repo_name}/forks'
    response = requests.get(url,auth=(st.secrets["GITHUB_NAME"], st.secrets["GITHUB_TOKEN"]))
    cnt = 0
    if response.status_code == 200:
        for _ in response.json():
            cnt += 1
        return cnt
    else:
        return None
    
@st.cache_data(show_spinner=False)
def get_stars(user_name,repo_name):
    url = f'https://api.github.com/repos/{user_name}/{repo_name}/stargazers'
    response = requests.get(url,auth=(st.secrets["GITHUB_NAME"], st.secrets["GITHUB_TOKEN"]))
    if response.status_code == 200:
        cnt = len(response.json())
        return cnt
    else:
        return None
    
@st.cache_data()
def get_followers(user_name):
    user_repos = []
    html_repos = []
    
    url = f'https://api.github.com/users/{user_name}/followers'
    response = requests.get(url,auth=(st.secrets["GITHUB_NAME"], st.secrets["GITHUB_TOKEN"]))
    if response.status_code == 200:
        for tmp_dict in response.json():
            user_repos.append(tmp_dict['login'])
            html_repos.append(tmp_dict['html_url'])
        return user_repos, html_repos
    else:
        return None
    
@st.cache_data(show_spinner=False)
def get_commits(user_name,repo_name):
    user_repos = []
    
    url = f'https://api.github.com/repos/{user_name}/{repo_name}/commits'
    response = requests.get(url,auth=(st.secrets["GITHUB_NAME"], st.secrets["GITHUB_TOKEN"]))
    if response.status_code == 200:
        for tmp_dict in response.json():
            user_repos.append(tmp_dict)
        return user_repos
    else:
        return None
    

@st.cache_data()
def get_url_list(user_name):
    url_repos = []
    
    url = f'https://api.github.com/users/{user_name}/repos'
    response = requests.get(url,auth=(st.secrets["GITHUB_NAME"], st.secrets["GITHUB_TOKEN"]))
    if response.status_code == 200:
        for tmp_dict in response.json():
            url_repos.append(tmp_dict['html_url'])
        return url_repos
    else:
        return None
    

# def check_api_limit():
#     url = f'https://api.github.com/rate_limit'
#     # api 리미트 체크용 -> 만일 auth 체크했다면 뺴야함 ..!
#     # response = requests.get(url,auth=("70cebd76ed1ad35e04e0", "919230fe025d4999b52f4bed63828f8c434d4788"))
#     return response.json()


# if __name__ == "__main__":
#     print(check_api_limit())
