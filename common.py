import streamlit as st
from streamlit.components.v1 import html

DEFAULT_SELECT_VALUE = "Select Repo"
MODEL_NAME = "gpt-3.5-turbo-16k"

def initialize_session():
    if not "initialized" in st.session_state:
        st.session_state["initialized"] = True
        st.session_state["repo_name"] = DEFAULT_SELECT_VALUE
        st.session_state["user_name"] = ""
        st.session_state["repo_url"] = ""
        st.session_state["visitied_list"] = []
        st.session_state["messages"] = []
        st.session_state["oai_key"] = ""


def handling_user_change():
    st.session_state["repo_name"] = DEFAULT_SELECT_VALUE
    st.session_state["repo_url"] = ""

def handling_openai_key_change():
    st.session_state["oai_key"] = ""

def buy_me_tea():
    button = """
    <script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="omijatea" data-color="#FFDD00" data-emoji="🍵"  data-font="Cookie" data-text="Buy me a tea" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#ffffff" ></script>
    """
    
    html(button, height=70, width=220)

    st.markdown(
        """
        <style>
            iframe[width="220"] {
                position: fixed;
                top: 50px;
                right: 30px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
