# Git-ter : GitHub QA Chatbot with Langchain

[Demo App Link](https://omijacha2.streamlit.app/)

Git-ter is short for <i>**"Feather: Rob a Github"**</i>, and has the same pronunciation as "Feather" in Korean.<br>
Git-ter is an analytical chatbot development framework dedicated to GitHub.<br>
Git-ter's goal is to **increase the productivity and efficiency of development** by helping shorten the time and effort to study through chatbot applications.

### Why Git-ter
- ChatGPT cannot learn the latest framework without web access extensions. So we created Git-ter, an application that can complement that.
- Using Langchain, which deals with Large Language Model(LLM). You can ask and answer specialized questions about the repository you entered.
- Store and retrieve data at high speed. Use FAISS, which is a Langchain vector store.

### Target Group
Anyone who is interested in programming looks at the GitHub repository.<br>
However, if there is too much content in the Repository, or if there is not enough explanation about the code, it's difficult to understand what it is. Or if you're new to coding, you're at a loss where to start looking at which files.

### Features
Git-ter is not just a chit-chat chatbot, provides file structure, code analysis, and summarization within the repository to make the content of the GitHub repository of interest easier to learn.

<br>

# DEMO
![GIT-TER_DEMO](https://github.com/SangHui48/GitHub-QA-Chatbot-with-Langchain/blob/jsm/video/GITTER_DEMO.webm)
![](https://github.com/SangHui48/GitHub-QA-Chatbot-with-Langchain/blob/master/video/demo2.gif)
![](https://github.com/SangHui48/GitHub-QA-Chatbot-with-Langchain/blob/master/video/demo3.gif)

<br>

# Git-ter Tutorial

### Use GPT 3.5-turbo-16k for
GitHub RestAPI, LangChain, FAISS(Vector DB) , OpenAI, and Streamlit.

## Development

1. Clone the repo or download the ZIP

```
git clone [github https url]
```

2. Install virtual environment and  packages

This repository runs for Python==3.9.13
```
1. conda create -n ENV_NAME python=3.9.13
2. conda activate ENV_NAME   
3. pip install -r requirements.txt   
```

3. Set up your `.env` file

- make ".streamlit/secrets.toml" file


```
GITHUB_NAME = 
GITHUB_TOKEN = 
OPENAI_API_KEY = 
```

- Visit [openai](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key) to retrieve API keys and insert into your `.streamlit/secrets.toml` file.
- Visit [github](https://docs.github.com/en/enterprise-server@3.6/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token) to create github access token

<br>

### Please Note
✨ Our application recommends using **Chrome**.<br>
✨ **If you run into errors, Open an issue.**<br>
✨ When you install and test the repository, you should change all of the names and tokens to `GITHUB_NAME` and  `GITHUB_TOKEN` at [get_info_from_api.py](https://github.com/SangHui48/GitHub-QA-Chatbot-with-Langchain/blob/master/githubqa/get_info_from_api.py).
```
# Example : get_info_from_api.py
# BEFORE
response = requests.get(url,auth=(st.secrets["GITHUB_NAME_1"], st.secrets["GITHUB_TOKEN_1"]))

# AFTER
response = requests.get(url,auth=(st.secrets["GITHUB_NAME"], st.secrets["GITHUB_TOKEN"]))
```

<br>

## Contributers
<table>
 <tr>
    <td align="center"><a href="https://github.com/holly-21"><img src="https://avatars.githubusercontent.com/holly-21" width="150px;" alt=""></td>
    <td align="center"><a href="https://github.com/aza1200"><img src="https://avatars.githubusercontent.com/aza1200" width="150px;" alt=""></td>
    <td align="center"><a href="https://github.com/furthermares"><img src="https://avatars.githubusercontent.com/furthermares" width="150px;" alt=""></td>
    <td align="center"><a href="https://github.com/SangHui48"><img src="https://avatars.githubusercontent.com/SangHui48" width="150px;" alt=""></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/holly-21"><b>Wonyoung</b></td>
    <td align="center"><a href="https://github.com/aza1200"><b>Jaehyeong</b></td>
    <td align="center"><a href="https://github.com/furthermares"><b>Sangmin</b></td>
    <td align="center"><a href="https://github.com/SangHui48"><b>Sanghui</b></td>
    </tr>
</table>
