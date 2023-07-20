import streamlit as st
import time

st.set_page_config(page_title="Gitter", page_icon="🪶")

st.markdown("# 깃-털(Gitter) : “깃헙을 털다.” 🧨\n")
st.sidebar.header("About Gitter 🪶")

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
st.markdown("## So What's it? 🤷")
st.write("""
         깃-털(Gitter)는 개발자들을 위한 **GitHub 분석 및 요약 챗봇 사이트**입니다. 챗봇을 통해 GitHub 저장소에 대한 깊은 통찰력을 제공합니다. 이를 통해 프로젝트의 구조, 파일명, 코드 등의 정보들을 빠르게  파악할 수 있도록 돕습니다.
         """)
st.markdown("\n")
st.write("**_깃-털을 통해 GitHub의 다양한 데이터를 분석하고 요약하여, 개발자들은 더 효율적인 개발과 협업을 이룰 수 있습니다._**")