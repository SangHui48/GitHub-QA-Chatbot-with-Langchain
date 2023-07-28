# Project Gitter

### Use GPT 3.5-turbo for 

GitHub RestAPI, LangChain, FAISS(Vector DB) , Openai, and Streamlit.

[DEMO video](./video/GITTER_DEMO.webm)

**If you run into errors, Open an issue**

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
