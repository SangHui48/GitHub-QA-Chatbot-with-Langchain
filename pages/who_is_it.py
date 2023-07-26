import requests
import pandas as pd
from common import *
from PIL import Image
import streamlit as st
from io import BytesIO
from githubqa.get_info_from_api import (
    get_repo_list, get_avatar_info,
    get_language_list, get_contributors,
    get_forks, get_followers,
    get_stars, get_commits, get_url_list
)

initialize_session()
buy_me_tea()

st.title('`Search User\'s Repo`')

st.session_state["user_name"] = st.sidebar.text_input(
    'GitHub User:',  key="github_user_input_search_whois", 
    value=st.session_state["user_name"],
    on_change=handling_user_change
    )

if st.session_state["user_name"]:
    user_name = st.session_state["user_name"]
    repo_list = get_repo_list(user_name)
    user_info = get_avatar_info(user_name)
    avatar_url = user_info['avatar_url']+'.png'
    image_response = requests.get(avatar_url)
    image = Image.open(BytesIO(image_response.content)).resize((250,250))
    st.sidebar.image(image, use_column_width='always', caption=f"{user_name}'s profile")
    # ======= User Info Table ========
    st.subheader("User Info")
    followers_name = get_followers(user_name)[0]
    followers_url = get_followers(user_name)[1]
    print([repo for repo in repo_list])
    df = pd.DataFrame(
        {
            "avartar": avatar_url,
            "e-mail": user_info['email'],
            "total repos": len(repo_list),
            "followers": [followers_name],
        }
    )
    
    st.dataframe(
        df,
        column_config={
            "avartar": st.column_config.ImageColumn("🤡 avartar", help="User's Github Avartar"),
            "e-mail": "📧 e-mail",
            "total repos": "👝 total repos",
            "followers": "🤝 followers"
        },
        hide_index=True,
    )

    if repo_list:
        # ======= All Repo Info Table ========
        with st.spinner('Getting User Information...'):
            st.subheader("User's Repositories")
            repo_name = [repo for repo  in repo_list if repo !=DEFAULT_SELECT_VALUE]
            languages = [get_language_list(user_name, repo) for repo in repo_name]
            contributors = [get_contributors(user_name, repo)[0] for repo in repo_name]
            forks = [get_forks(user_name, repo) for repo in repo_name]
            stars = [get_stars(user_name, repo) for repo in repo_name]
            repo_url = [url for url in get_url_list(user_name)]
        
        # 날짜 별 commit 수 flow chart
        commits = [get_commits(user_name, repo) for repo in repo_name]
        commit_list = []
        for i in range(len(commits)):
            commits_dict={}
            for j in range(len(commits[i])):
                commit_date = commits[i][j]['commit']['author']['date'][:10]
                if commits_dict.get(commit_date): commits_dict[commit_date] += 1
                else: commits_dict[commit_date] = 1
            commits_dict = sorted(commits_dict.items())
            commit_list.append(commits_dict)
            
        df = pd.DataFrame(
            {
                "name": repo_name,
                "url": repo_url,
                "stars": stars,
                "views_history": [[commit[1] for commit in commits] for commits in commit_list],
                "contributers": contributors,
                "language": languages,
            }
        )

        st.dataframe(
            df,
            column_config={
                "name": "GitHub name",
                "stars": st.column_config.NumberColumn(
                    "GitHub Stars",
                    help="Number of stars on GitHub",
                    format="%d ⭐",
                ),
                "url": st.column_config.LinkColumn("GitHub URL"),
                "views_history": st.column_config.LineChartColumn(
                    "Views (past 30 days)", y_min=0, y_max=30
                ),
                "contributers": "contributors",
                "language": "languages",
            },
            hide_index=True,
        )
    else:
        st.error("Invalid user ID")