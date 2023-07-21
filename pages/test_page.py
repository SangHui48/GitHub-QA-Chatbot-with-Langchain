import requests
from PIL import Image
from io import BytesIO
import streamlit as st
from pages.file_viewer import print_directory_structure
from githubqa.get_info_from_api import get_repo_list, get_avatar_info


user = st.text_input('GitHub User:', key="github_user_input")
if user:
    repo_list = get_repo_list(user)
    user_info = get_avatar_info(user)
    if repo_list:
        specific_repo = st.selectbox(f"Select {user}'s repository", repo_list, key="repo_select")
        avatar_url = user_info['avatar_url']
        image_response = requests.get(avatar_url)
        image = Image.open(BytesIO(image_response.content)).resize((250,250))
        st.write('You selected:', specific_repo)
        st.write(user_info)
        st.image(image, caption=f"{user}'s profile")
        print_directory_structure(user, specific_repo)
    else:
        st.error("Invalid user ID")