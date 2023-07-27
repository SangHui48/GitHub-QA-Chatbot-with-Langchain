import os
import time
import requests
from common import *
from PIL import Image
from io import BytesIO
import streamlit as st
from githubqa.vector_db import *
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from githubqa.data_processing import dictionary_to_docs
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from githubqa.get_info_from_api import get_avatar_info, get_repo_list, github_api_call

# 1. Session Initialize & Donation
initialize_session()
buy_me_tea()

# 2. Sidebar username input
st.session_state['oai_key'] = st.sidebar.text_input(
    'Open API KEY:',  key="open_api", 
    value=st.session_state["oai_key"],
    on_change=handling_openai_key_change,
    type="password"
    )
if st.session_state['oai_key']:
    os.environ['OPENAI_API_KEY'] = st.session_state['oai_key']

st.sidebar.title('`Gitter`:feather:')
st.session_state["user_name"] = st.sidebar.text_input(
    'GitHub User:',  key="github_user_input", 
    value=st.session_state["user_name"],
    on_change=handling_user_change
    )
# 3. Sidebar Select Repo + User Avatar layout
if st.session_state["user_name"]:
    user_name = st.session_state['user_name']
    repo_list = get_repo_list(user_name)[0]
    user_info = get_avatar_info(user_name)
    if repo_list:
        repo_list = [DEFAULT_SELECT_VALUE] + repo_list 
        st.session_state["repo_name"] = st.sidebar.selectbox(
                f"Select {user_name}'s repository", repo_list, 
                key="repo_select",
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
st.sidebar.info('Made with  by [오미자차](https://github.com/SangHui48/KDT_AI_B3)')


# 4. Main Screen Start 
st.header("`Chatbot`")
if st.session_state['repo_url']:
    with st.spinner('Analyzing Repository...'):
        # Return Value : "File_name" : "File_content"
        github_info_dict, structure_content, _, user_content = github_api_call(st.session_state['repo_url'])
        
    # Return Values [Doc1, Doc2 ...]
    with st.spinner('Embedding to VectorSpace...'):
        docs = dictionary_to_docs(
            github_info_dict, structure_content, user_content,
            chunking_size=1000, overlap_size=0, 
            model_name=MODEL_NAME
        )
        # Chunked Data to Vector embedding 
        embedding_model = OpenAIEmbeddings(model='text-embedding-ada-002')

        if st.session_state['repo_url'] not in st.session_state['visitied_list']:
            vector_db = db_from_pinecone(docs, embedding_model)
            st.session_state['vector_db'] = vector_db
            st.session_state['visitied_list'].append(st.session_state['repo_url'])
            st.session_state['messages'] = []
        else:
            vector_db =  st.session_state['vector_db']

    # Retriever setting for Question_Answering 
    retriever =  mmr_retriever_setting(
        vectorstore=vector_db, 
        fetch_num=10, k_num=100
    )
    open_ai_model =  ChatOpenAI(model_name=MODEL_NAME)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=open_ai_model,
        memory=memory,
        retriever=retriever,
        get_chat_history=lambda h : h,
    )

    # QA Start 
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask questions about the GitHub repository!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.spinner('Generating answers...'):
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                response = qa_chain({"question": prompt}) # QA chain
                for response in response['answer']:
                    full_response += response
                    time.sleep(0.02)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
else:
    st.info('Hit your **GITHUB NAME** and **REPO** to the left side bar.')
    st.info("""
            I am an analysis tool for question-answering built on LangChain.\n
            Given GitHub informations, I will analyze the repository using LangChain and store it in vectorDB.
            And I will answer questions about GitHub through openAI.\n
            For example, I respond to information about the structure of the git repository, what it does, and what functions are in.\n
            Here is the video of example. 
            """)
    st.video("video/GITTER_DEMO.webm", format="video/webm")