import streamlit as st
import pandas as pd
from common import *

st.set_page_config(page_title="Gitter", page_icon="🪶")
buy_me_tea()

st.sidebar.header("About Git-ter 🪶")

df = pd.DataFrame({
    'GitHub': ['https://github.com/holly-21', 'https://github.com/aza1200', 'https://github.com/furthermares', 'https://github.com/SangHui48']
}, index=['박원영', '김재형', '전상민', '한상희'])

def make_clickable(link):
    text = link.split('/')[-1]
    return f'<a target="_blank" href="{link}">{text}</a>'

df['GitHub'] = df['GitHub'].apply(make_clickable)
df = df.to_html(escape=False)
st.sidebar.write(df, unsafe_allow_html=True)


tab1, tab2 = st.tabs(["Korean", "English"])

with tab1:
    st.markdown("# 깃-털(Gitter) : “깃헙을 털다.” 🧨\n")

    st.markdown('## For Whom 🧐')
    st.write("""
            - 새로운 개발 프로젝트를 시작하시는 분
            - 새로운 오픈 소스를 뜯어보시는 분
            """)
    st.markdown("## Use When 👨‍💻")
    st.write("""
            개발을 하다 보면 GitHub Repository를 통해 개발 공부를 해야합니다.\n
            다들 어떤 폴더에서 어떤 파일에 가야 내가 원하는 내용이 있는지를 찾았던 적이 있나요?\n
            그 과정들을 위해 폴더 하나하나, 파일 하나하나 모두 찾아봐야 했던 적이 있나요?\n\n
            """)
    st.markdown("## So, what is it? 🤷")
    st.write("""
            깃-털(Gitter)는 개발자들을 위한 **GitHub 분석 및 요약 챗봇 사이트**입니다. 챗봇을 통해 GitHub 저장소에 대한 깊은 통찰력을 제공합니다. 이를 통해 프로젝트의 구조, 파일명, 코드 등의 정보들을 빠르게  파악할 수 있도록 돕습니다.
            """)
    st.markdown("\n")
    st.write("**_깃-털을 통해 GitHub의 다양한 데이터를 분석하고 요약하여, 개발자들은 더 효율적인 개발과 협업을 이룰 수 있습니다._**")

with tab2:
    st.markdown("# Git-ter : GitHub QA Chatbot with Langchain 🧨\n")

    st.write("""
            Git-ter is short for **"Feather: Rob a Github"**, and has the same pronunciation as "Feather" in Korean.\n
            Git-ter is an analytical chatbot development framework dedicated to GitHub.\n
            Git-ter's goal is to **increase the productivity and efficiency of development** by helping shorten the time and effort to study through chatbot applications.
            """)

    st.markdown('## Why Git-ter 🧐')
    st.write("""
            - ChatGPT cannot learn the latest framework without web access extensions. So we created Git-ter, an application that can complement that.
            - Using Langchain, which deals with Large Language Model(LLM). You can ask and answer specialized questions about the repository you entered.
            - Store and retrieve data at high speed. Use FAISS, which is a Langchain vector store.
            """)
    st.markdown("## Target Group ")
    st.write("""
            Anyone who is interested in programming looks at the GitHub repository.\n
            However, if there is too much content in the Repository, or if there is not enough explanation about the code, it's difficult to understand what it is. Or if you're new to coding, you're at a loss where to start looking at which files.\n\n
            """)
    st.markdown("\n")
    st.markdown("## Features")
    st.markdown("""
                *Git-ter is not just a chit-chat chatbot, provides file structure, code analysis, and summarization within the repository to make the content of the GitHub repository of interest easier to learn.*
                """)