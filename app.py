import time
from PIL import Image
from io import BytesIO
import requests
import streamlit as st
from githubqa.vector_db import *
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from githubqa.get_info_from_api import get_avatar_info, get_repo_list, github_api_call
from githubqa.data_processing import dictionary_to_docs
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain

if "repo_url" not in st.session_state:
    st.session_state['repo_url'] = ""

# Sidebar contents
st.sidebar.title('`Gitter`:feather:')
github_user = st.sidebar.text_input("`Github User ID:`")
if github_user:
    repo_list = get_repo_list(github_user)
    user_info = get_avatar_info(github_user)
    if repo_list:
        specific_repo = st.sidebar.selectbox(f"Select {github_user}'s repository", repo_list, key="repo_select")
        avatar_url = user_info['avatar_url']
        image_response = requests.get(avatar_url)
        image = Image.open(BytesIO(image_response.content)).resize((250,250))
        st.sidebar.success(f'`You selected:{specific_repo}`')
        # st.sidebar.write(user_info)
        st.sidebar.image(image, use_column_width='always', caption=f"{github_user}'s profile")
        st.session_state['repo_url'] = f"https://github.com/{github_user}/{specific_repo}"
    else:
        st.error("Invalid user ID")

st.sidebar.info('Made with  by [오미자차](https://github.com/SangHui48/KDT_AI_B3)')

def main():
    MODEL_NAME = "gpt-3.5-turbo-16k" # langchain llm config

    st.header("`Chatbot`")

    # user input github repo url
    # github_link = st.text_input("Github repository link을 입력해주세요")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if st.session_state['repo_url']:
        if 'vector_db' not in st.session_state: 
            with st.spinner('레포지터리 분석중...'):
                # 2. 모든 데이터 "File_name" : "File_content" 형식 받아오기
                github_info_dict, structure_content, _ = github_api_call(st.session_state['repo_url'])
                # print(github_info_dict)
            # 3. "File_content 형식 데이터" 청킹 갯수 단위로 자른후에 리스트로 변환하기
            # 반환값 [Doc1, Doc2 ...]
            with st.spinner('임베딩중...'):
                print(len(github_info_dict.keys()))
                docs = dictionary_to_docs(
                    github_info_dict, structure_content,
                    chunking_size=1000, overlap_size=0, 
                    model_name=MODEL_NAME
                )
                # 4. chunking 된 데이터 vector db 로 임베딩 하기 
                # 임베딩 모델 및 vector db 반환 
                embedding_model = OpenAIEmbeddings(model='text-embedding-ada-002')
                # vector_db = db_from_deeplake(docs, embedding_model)
                vector_db = db_from_pinecone(docs, embedding_model)
                st.session_state['vector_db'] = vector_db
        else:
            vector_db =  st.session_state['vector_db']
        # 5. QA 를 위한 retriever 및 qa 세팅 하기
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
        #QA 시작
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask questions about the GitHub repository!"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.spinner('답변 생성중...'):
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
        
        # query = st.chat_input("Your message: ", key="user_input")
        # if query:
        #     st.session_state.messages.append(query)
        #     with st.spinner("답변 생성중..."):
        #         response = qa_chain({"question": query})
        #         st.session_state.messages.append(response["answer"])
                    
        #     messages = st.session_state.get('messages', [])
        #     for i, msg in enumerate(messages):
        #         if i % 2 == 0:
        #             with st.chat_message("user"):
        #                 st.write(msg, key=str(i) + '_user')
        #         else:
        #             with st.chat_message("assistant"):
        #                 # st.write(msg, key=str(i) + '_ai')

        #                 # Answer UI
        #                 # import time
        #                 message_placeholder = st.empty()
        #                 full_response = ""
        #                 # Simulate stream of response with milliseconds delay
        #                 for chunk in msg.split():
        #                     full_response += chunk
        #                     # time.sleep(0.05)  
        #                     # Add a blinking cursor to simulate typing
        #                     message_placeholder.markdown(full_response + "▌")
        #                 message_placeholder.markdown(full_response)
    else:
        st.error('Please check Username and Repository name.')
if __name__ == '__main__':
    main()