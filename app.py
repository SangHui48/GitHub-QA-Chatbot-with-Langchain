import streamlit as st
from dotenv import load_dotenv
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from githubqa.data_processing import dictionary_to_docs
from githubqa.get_info_from_api import github_api_call
from githubqa.vector_db import (
    db_from_pinecone, db_from_deeplake, mmr_retriever_setting
)

# Sidebar contents
with st.sidebar:
    st.set_page_config(page_title = "This is a Multipage WebApp")
    st.title('🤗💬 LLM Chat App')
    add_vertical_space(5)
    st.write('Made with  by [오미자차](https://github.com/SangHui48/KDT_AI_B3)')
    

def main():
    load_dotenv()
    MODEL_NAME = "gpt-3.5-turbo-16k" # langchain llm config

    st.header("Gitter:feather: ")

    # user input github repo url
    github_link = st.text_input("Github repository link을 입력해주세요")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if github_link:
        with st.spinner('레포지터리 분석중...'):
            # 2. 모든 데이터 "File_name" : "File_content" 형식 받아오기
            github_info_dict, structure_content = github_api_call(github_link)

        # 3. "File_content 형식 데이터" 청킹 갯수 단위로 자른후에 리스트로 변환하기
        # 반환값 [Doc1, Doc2 ...]
        with st.spinner('임베딩중...'):
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
        query = st.chat_input("Your message: ", key="user_input")
        if query:
            st.session_state.messages.append(query)
            with st.spinner("답변 생성중..."):
                response = qa_chain({"question": query})
                st.session_state.messages.append(response["answer"])
                    
            messages = st.session_state.get('messages', [])
            for i, msg in enumerate(messages):
                if i % 2 == 0:
                    with st.chat_message("user"):
                        st.write(msg, key=str(i) + '_user')
                else:
                    with st.chat_message("assistant"):
                        st.write(msg, key=str(i) + '_ai')

if __name__ == '__main__':
    main()