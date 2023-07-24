import streamlit as st

if not "initialized" in st.session_state:
    st.session_state.return_values = []
    st.session_state.change_values = []
    st.session_state.initialized = True
    st.session_state.first_return = True

def capture_change_value():
    st.session_state.change_values.append(st.session_state.number)
    st.text(f"Change values: {st.session_state.change_values}")

def capture_return_value(number):
    if st.session_state.first_return:
        capture_change_value()
        st.session_state.first_return = False

    st.session_state.return_values.append(number)
    st.text(f"Return values: {st.session_state.return_values}")

capture_return_value(st.number_input("Number", key="number", on_change=capture_change_value))

# import requests
# from PIL import Image
# from io import BytesIO
# import streamlit as st
# from pages.file_viewer import print_directory_structure
# from githubqa.get_info_from_api import get_repo_list, get_avatar_info

# DEFAULT_SELECT_VALUE = "Select Repo"

# user = st.text_input('GitHub User:', key="github_user_input")
# if user:
#     repo_list = get_repo_list(user)
#     user_info = get_avatar_info(user)
#     if repo_list:
#         repo_list = [DEFAULT_SELECT_VALUE] + repo_list 
#         specific_repo = st.selectbox(
#             f"Select {user}'s repository", 
#             repo_list, 
#             key="repo_select"
#         )
#         if specific_repo != DEFAULT_SELECT_VALUE:
#             avatar_url = user_info['avatar_url']
#             image_response = requests.get(avatar_url)
#             image = Image.open(BytesIO(image_response.content)).resize((250,250))
#             st.write('You selected:', specific_repo)
#             st.write(user_info)
#             st.image(image, caption=f"{user}'s profile")
#             print_directory_structure(user, specific_repo)
#     else:
#         st.error("Invalid user ID")